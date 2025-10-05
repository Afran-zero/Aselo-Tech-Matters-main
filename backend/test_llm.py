import os
import json
from datetime import datetime
import asyncio
from typing import Dict, Any, Optional
from app.models.conversation_model import ChatMessage
from app.services.llm_service import llm_service


def build_complete_summary(
    summary_text: str,
    conversation_metadata: Dict[str, Any],
    is_repeat_caller: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Build complete summary object combining:
    - AI-generated summary
    - Conversation-derived metadata
    - System metadata (repeat caller)
    - Placeholders for post-call fields
    """
    
    summary = {
        "callSummary": summary_text,
        
        # These CAN be extracted from conversation
        "locationOfIssue": conversation_metadata.get("locationOfIssue"),
        "actionTaken": conversation_metadata.get("actionTaken"),
        "outcomeOfContact": conversation_metadata.get("outcomeOfContact"),
        "howDidYouKnowAboutOurLine": conversation_metadata.get("howDidYouKnowAboutOurLine"),
        "okForCaseWorkerToCall": conversation_metadata.get("okForCaseWorkerToCall"),
        "didTheChildFeelWeSolvedTheirProblem": conversation_metadata.get("didTheChildFeelWeSolvedTheirProblem"),
        "wouldTheChildRecommendUsToAFriend": conversation_metadata.get("wouldTheChildRecommendUsToAFriend"),
        "didYouDiscussRightsWithTheChild": conversation_metadata.get("didYouDiscussRightsWithTheChild"),
        
        # System-level check
        "repeatCaller": is_repeat_caller,
        
        # Always true for helpline
        "keepConfidential": True,
        
        # These MUST be filled by counselor AFTER the call
        "summaryAccuracy": None,
        "summaryFeedback": None,
        "otherLocation": None,
    }
    
    return summary


def print_extraction_report(
    child: Dict[str, Any],
    categories: Dict[str, Any],
    summary: Dict[str, Any],
    conversation_metadata: Dict[str, Any]
):
    """Print a detailed extraction report."""
    
    print("\n" + "="*70)
    print("EXTRACTION REPORT")
    print("="*70)
    
    # Child Information
    print("\n📋 CHILD INFORMATION:")
    print(f"  Name: {child.get('firstName', 'N/A')} {child.get('lastName', 'N/A')}")
    print(f"  Gender: {child.get('gender') or 'Not specified'}")
    print(f"  Age: {child.get('age') or 'Not specified'}")
    print(f"  Parish: {child.get('parish') or 'Not specified'}")
    print(f"  Region: {child.get('region') or 'Not specified'}")
    print(f"  Nationality: {child.get('nationality') or 'Not specified'}")
    
    if child.get('streetAddress'):
        print(f"  Address: {child['streetAddress']}")
    
    if child.get('phone1'):
        print(f"  Phone 1: {child['phone1']}")
    if child.get('phone2'):
        print(f"  Phone 2: {child['phone2']}")
    
    # Education
    print("\n🎓 EDUCATION:")
    print(f"  School: {child.get('schoolName') or 'Not specified'}")
    print(f"  Grade: {child.get('gradeLevel') or 'Not specified'}")
    
    # Living Situation
    print("\n🏠 LIVING SITUATION:")
    print(f"  Situation: {child.get('livingSituation') or 'Not specified'}")
    if child.get('vulnerableGroups'):
        print(f"  Vulnerable Groups: {', '.join(child['vulnerableGroups'])}")
    
    # Categories
    print("\n🏷️  ISSUE CATEGORIES:")
    if categories:
        for category, issues in categories.items():
            print(f"  • {category}: {', '.join(issues)}")
    else:
        print("  No categories identified")
    
    # Conversation Metadata
    print("\n📊 CONVERSATION METADATA:")
    metadata_fields = [
        ("Location of Issue", conversation_metadata.get("locationOfIssue")),
        ("Action Taken", conversation_metadata.get("actionTaken")),
        ("Outcome", conversation_metadata.get("outcomeOfContact")),
        ("How Found Us", conversation_metadata.get("howDidYouKnowAboutOurLine")),
        ("OK for Follow-up", conversation_metadata.get("okForCaseWorkerToCall")),
        ("Problem Solved", conversation_metadata.get("didTheChildFeelWeSolvedTheirProblem")),
        ("Would Recommend", conversation_metadata.get("wouldTheChildRecommendUsToAFriend")),
        ("Rights Discussed", conversation_metadata.get("didYouDiscussRightsWithTheChild")),
    ]
    
    for label, value in metadata_fields:
        if value is not None:
            display_value = str(value) if not isinstance(value, bool) else ("Yes" if value else "No")
            print(f"  • {label}: {display_value}")
    
    # Summary
    print("\n📝 CALL SUMMARY:")
    summary_text = summary.get("callSummary", "")
    if summary_text:
        # Word wrap at 70 characters
        words = summary_text.split()
        line = "  "
        for word in words:
            if len(line) + len(word) + 1 > 72:
                print(line)
                line = "  " + word
            else:
                line += (" " if line != "  " else "") + word
        if line.strip():
            print(line)
    
    # Data Completeness
    print("\n📈 DATA COMPLETENESS:")
    
    total_child_fields = 14
    filled_child = sum(1 for v in child.values() if v is not None and v != "")
    print(f"  Child Info: {filled_child}/{total_child_fields} fields ({filled_child/total_child_fields*100:.0f}%)")
    
    metadata_count = sum(1 for v in conversation_metadata.values() if v is not None)
    total_metadata = 8
    print(f"  Metadata: {metadata_count}/{total_metadata} fields ({metadata_count/total_metadata*100:.0f}%)")
    
    # Fields Requiring Manual Input
    print("\n⚠️  REQUIRES COUNSELOR INPUT (Post-Call):")
    manual_fields = [
        "  • summaryAccuracy - Counselor must review and rate AI summary",
        "  • summaryFeedback - Counselor's corrections or additional notes"
    ]
    if summary.get("locationOfIssue") == "Other":
        manual_fields.append("  • otherLocation - Specify the exact location")
    
    print("\n".join(manual_fields))
    
    print("\n" + "="*70)


async def check_repeat_caller(first_name: Optional[str], phone: Optional[str]) -> Optional[bool]:
    """
    Check if this is a repeat caller by querying database.
    In production, this would query your actual database.
    
    For now, returns None (unknown).
    """
    # TODO: Implement database check
    # Example:
    # if phone:
    #     existing = await db.query("SELECT * FROM calls WHERE phone1 = ?", phone)
    #     return len(existing) > 0
    return None


async def main():
    """Main test function to extract all data from conversation."""
    
    # Load conversation from local_db.json
    db_path = os.path.join(os.path.dirname(__file__), "database", "local_db.json")
    
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Could not find database file at {db_path}")
        print(f"   Expected path: {db_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in database file: {e}")
        return
    
    # Convert message dicts to ChatMessage objects
    messages = []
    for msg in data.get("messages", []):
        try:
            ts_str = msg["timestamp"]
            if ts_str.endswith("Z"):
                ts = datetime.fromisoformat(ts_str[:-1] + "+00:00")
            else:
                ts = datetime.fromisoformat(ts_str)
            
            messages.append(
                ChatMessage(
                    id=msg["id"],
                    sender=msg["sender"],
                    message=msg["message"],
                    timestamp=ts
                )
            )
        except Exception as e:
            print(f"⚠️  Warning: Skipping malformed message: {e}")
            continue
    
    if not messages:
        print("❌ Error: No valid messages found in database")
        return
    
    print(f"\n🚀 Starting extraction for {len(messages)} messages...")
    print("="*70)
    
    # --- Stage 1: Extract child data and categories ---
    print("\n🔍 Stage 1: Extracting child information and categories...")
    try:
        autofill = await llm_service.extract_form_data(messages)
        print("   ✅ Child data extracted")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        return
    
    # --- Stage 2: Generate summary ---
    print("\n📝 Stage 2: Generating call summary...")
    try:
        summary_text = await llm_service.generate_summary(messages)
        print("   ✅ Summary generated")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        summary_text = "Summary generation failed"
    
    # --- Stage 3: Extract conversation metadata ---
    print("\n🔍 Stage 3: Analyzing conversation for metadata...")
    try:
        conversation_metadata = await llm_service.extract_conversation_metadata(messages)
        print("   ✅ Metadata extracted")
    except Exception as e:
        print(f"   ⚠️  Warning: Metadata extraction failed: {e}")
        conversation_metadata = {}
    
    # --- Stage 4: Check system metadata ---
    print("\n🗄️  Stage 4: Checking system metadata...")
    is_repeat_caller = await check_repeat_caller(autofill.firstName, autofill.phone1)
    if is_repeat_caller is None:
        print("   ℹ️  Repeat caller status: Unknown (no database check implemented)")
    else:
        print(f"   ✅ Repeat caller: {'Yes' if is_repeat_caller else 'No'}")
    
    # --- Build complete form data ---
    print("\n🔨 Building complete form data structure...")
    
    child = {
        "firstName": autofill.firstName,
        "lastName": autofill.lastName,
        "gender": autofill.gender,
        "age": autofill.age,
        "streetAddress": autofill.streetAddress,
        "parish": autofill.parish,
        "phone1": autofill.phone1,
        "phone2": autofill.phone2,
        "nationality": autofill.nationality,
        "schoolName": autofill.schoolName,
        "gradeLevel": autofill.gradeLevel,
        "livingSituation": autofill.livingSituation,
        "vulnerableGroups": autofill.vulnerableGroups,
        "region": autofill.region
    }
    
    summary = build_complete_summary(
        summary_text,
        conversation_metadata,
        is_repeat_caller
    )
    
    form_data = {
        "child": child,
        "category": autofill.suggested_categories or {},
        "summary": summary
    }
    
    # --- Display Results ---
    print_extraction_report(child, autofill.suggested_categories or {}, summary, conversation_metadata)
    
    # --- JSON Output ---
    output = {"formData": form_data}
    
    print("\n" + "="*70)
    print("JSON OUTPUT")
    print("="*70)
    print(json.dumps(output, indent=2, ensure_ascii=False))
    
    # --- Save to file ---
    output_path = os.path.join(os.path.dirname(__file__), "extracted_data.json")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Output saved to: {output_path}")
    except Exception as e:
        print(f"\n⚠️  Warning: Could not save output file: {e}")
    
    # --- Additional Tips ---
    print("\n" + "="*70)
    print("💡 TIPS")
    print("="*70)
    print("• Fields with 'null' values were not found in the conversation")
    print("• Smart defaults were applied where reasonable (gender from name, etc.)")
    print("• Some fields require manual counselor input after the call")
    print("• Review 'summaryAccuracy' to validate the AI-generated summary")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()