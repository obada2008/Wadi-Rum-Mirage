"""Adds case-specific educational interpretation, without making verification claims."""
import re

def build_report(result, message):
    kinds = {x['type'] for x in result['sensitive_actions']}
    tips = []
    if 'otp_disclosure' in kinds or 'password_disclosure' in kinds:
        tips.append({'title':'أوقف مشاركة بيانات الدخول','detail':'رموز التحقق وكلمات المرور لا تُشارك عبر الرسائل أو المكالمات.'})
    if 'payment' in kinds:
        tips.append({'title':'تحقق من الرسوم','detail':'راجع الجهة بنفسك عبر قنوات موثقة قبل أي دفع.'})
    if result['urls_detected']:
        tips.append({'title':'تحقق من عنوان الموقع','detail':'لا تفترض أن رابطاً تابع لجهة لمجرد ذكر اسمها؛ اكتب العنوان الرسمي بنفسك.'})
    if result['trust_transfers']:
        tips.append({'title':'افصل الادعاء عن الإجراء','detail':'صحة وجود مؤسسة أو خدمة لا تثبت أن الجهة أرسلت هذا الطلب.'})
    if not tips:
        tips.append({'title':'لا تتعامل مع النتيجة كضمان','detail':'عدم رصد مؤشر لا يعني أن الرسالة سليمة؛ تحقق مستقلاً عند الشك.'})
    result['educational_explanations'] = tips
    result['analysis_method'] = 'deterministic_rules'
    result['verification_performed'] = False
    result['privacy_note'] = 'لا يخزن الخادم نص الرسالة ولا يزور روابطها.'
    return result
