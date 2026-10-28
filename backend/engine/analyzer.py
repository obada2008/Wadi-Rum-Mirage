"""Wadi Rum Mirage — deterministic, explainable Arabic safety analysis.
No network calls, URL fetching, or text storage.
"""
import re
import uuid
from urllib.parse import urlsplit

AR_DIACRITICS = re.compile(r'[\u064b-\u065f\u0670ـ]')
URL_PATTERN = re.compile(r'(?:https?://|www\.)[^\s<>"\']+', re.IGNORECASE)

ACTION_PATTERNS = [
    ('otp_disclosure', r'(?:رمز\s*(?:التحقق|التاكيد|التفعيل|otp)|كود\s*(?:التحقق|التاكيد|otp)|\botp\b|verification\s*code|one[ -]?time\s*(?:password|code)|2fa\s*code|security\s*code)', 45, 'مشاركة رمز التحقق قد تسمح بالاستيلاء على الحساب.'),
    ('password_disclosure', r'(?:كلمه\s*(?:المرور|السر)|password|passcode|login\s*credentials|الباسورد)', 45, 'لا تشارك كلمات المرور عبر الرسائل.'),
    ('payment', r'(?:ادفع|دفع\s*(?:رسوم|مبلغ)|حول\s*(?:المبلغ|فلوس|مصاري)|رسوم\s*(?:التفعيل|التسجيل)|حواله|بطاقتك\s*البنكيه|pay\s+(?:the\s+|a\s+)?(?:activation\s+)?(?:fee|deposit)|payment|transfer\s*(?:money|funds)|activation\s*fee|credit\s*card|bank\s*details)', 28, 'تحقق من جهة التحصيل وشرعية الرسوم بشكل مستقل.'),
    ('identity_data', r'(?:الرقم\s*الوطني|رقم\s*الهويه|بياناتك\s*الشخصيه|صوره\s*الهويه|صورة\s*هويتك|national\s*id|identity\s*(?:card|document)|personal\s*(?:data|information)|passport\s*(?:photo|number))', 23, 'لا تفصح عن بيانات الهوية إلا عبر قناة تتحقق منها بشكل مستقل.'),
]
PROMPT_PATTERNS = [r'\b(?:ارسل|ابعت|ادخل|اكتب|شارك|زودنا|سجل|فعّل|فعل|اضغط|افتح|حوّل|حول|ادفع|قدم|زودني)\b', r'\b(?:send|enter|share|submit|click|verify|pay|transfer|provide|upload|activate|confirm|reply|type|follow|claim|complete|update)\b']
AUTHORITY = r'(?:وزاره|حكوم[يه]|مؤسس[هت]|دائره|جامع[هت]|رسمي[هت]?|البنك|البريد\s*الاردني|الضمان|الجامعه|المنصه|شرك[هت]|\b(?:government|ministry|official|agency|university|bank|company|institution|tax\s*authority|postal\s*service|support\s*team)\b)'
TRUST_CONNECTORS = r'(?:ولهيك|لذلك|وبالتالي|وعشان\s*هيك|لهذا|بناء\s*على|بما\s*ان|ومن\s*ثم|عشان|إذن|اذن|للاستفاده|للاستفادة|\b(?:therefore|so\s+(?:you\s+)?(?:must|need)|because|hence|as\s+a\s+result|to\s+(?:activate|claim|receive)|in\s+order\s+to)\b)'
URGENCY = r'(?:فورا|فوراً|الان|حالاً|خلال\s*\d+\s*(?:ساع|دقيق)|آخر\s*فرصه|اخر\s*فرصه|قبل\s*انتهاء|سيتم\s*ايقاف|رح\s*ينلغي|\b(?:immediately|urgent|right\s*now|within\s*\d+\s*(?:hours|minutes)|last\s*chance|account\s*(?:will\s*be\s*)?(?:blocked|suspended)|expires\s*today)\b)'
NEGATION = r'(?:لا\s+ت(?:رسل|بعت|دخل|شارك|عطي|ضغط)|اياك\s+ت|احذر\s+من|ممنوع\s+ت|تجنب\s+مشارك|ما\s+ت(?:رسل|بعت|شارك|عطي|دخل)|لا\s+تقم\s+بمشارك|\b(?:do\s+not|don.t|never|avoid)\s+(?:send|share|enter|provide|reveal|disclose|give|type|submit)\b|\b(?:beware|watch\s*out\s*for)\b)'


def normalize(text: str) -> str:
    text = AR_DIACRITICS.sub('', text.lower())
    return text.translate(str.maketrans({'أ':'ا','إ':'ا','آ':'ا','ى':'ي','ة':'ه','ؤ':'و','ئ':'ي'}))


def has(pattern, text):
    return bool(re.search(pattern, text, re.IGNORECASE))


def analyze(message: str):
    if not isinstance(message, str) or not message.strip():
        raise ValueError('الرسالة مطلوبة')
    if len(message) > 5000:
        raise ValueError('الحد الأقصى 5000 حرف')
    normalized = normalize(message)
    urls = [u.rstrip('.,،؛)') for u in URL_PATTERN.findall(message)]
    # Avoid treating warnings about scams as requests to share secrets.
    # A warning in one sentence should not neutralize an unrelated request elsewhere.
    clauses = [c.strip() for c in re.split(r'[.!؟\n؛]+', normalized) if c.strip()]
    requests = [c for c in clauses if has('|'.join(PROMPT_PATTERNS), c) and not has(NEGATION, c)]
    is_warning = has(NEGATION, normalized) and not requests
    directives = has('|'.join(PROMPT_PATTERNS), normalized)
    authority = has(AUTHORITY, normalized)
    bridge = has(TRUST_CONNECTORS, normalized)
    urgency = has(URGENCY, normalized)
    detected = []
    for kind, pattern, weight, explanation in ACTION_PATTERNS:
        if has(pattern, normalized):
            detected.append({'type':kind, 'explanation':explanation, 'sensitive':True, 'weight':weight})
    asking_sensitive = bool(detected) and bool(requests) and not is_warning
    rules = []
    if asking_sensitive:
        for d in detected:
            rid = {'otp_disclosure':'R01','password_disclosure':'R01','payment':'R03','identity_data':'R06'}[d['type']]
            rules.append({'id':rid,'title':d['type'],'reason':d['explanation'],'weight':d['weight']})
    if urls and authority and not is_warning:
        rules.append({'id':'R02','title':'نسبة رابط إلى جهة','reason':'ذكر اسم جهة لا يثبت ملكيتها للرابط. لم يتم فتح الرابط أو التحقق منه.','weight':14})
    if urgency and asking_sensitive:
        rules.append({'id':'R04','title':'ضغط زمني','reason':'يجمع النص بين استعجال وطلب بيانات أو إجراء حساس.','weight':15})
    transfer = bool(authority and asking_sensitive and (bridge or bool(urls)))
    if transfer:
        rules.append({'id':'R05','title':'انتقال ثقة غير مدعوم','reason':'الحديث عن جهة أو خدمة لا يثبت أن الإجراء المطلوب مخوّل من تلك الجهة.','weight':22})
    score = min(100, sum(r['weight'] for r in rules))
    if transfer or score >= 45:
        status = 'warning'
        title = 'مؤشرات خطر مرتفعة — تحقق قبل التصرف'
    elif score > 0:
        status = 'caution'
        title = 'هناك مؤشرات تستدعي التحقق'
    else:
        status = 'insufficient' if (authority or urls or detected) and not is_warning else 'no_indicators'
        title = 'الأدلة غير كافية للحكم' if status == 'insufficient' else 'لم تُرصد مؤشرات بالقواعد الحالية'
    nodes = [{'id':'message','label':'نص الرسالة','type':'message'}]
    edges = []
    if authority:
        nodes.append({'id':'claim','label':'ادعاء / جهة مذكورة','type':'claim','verification':'unknown'})
        edges.append({'source':'message','target':'claim','type':'contains'})
    if urls:
        nodes.append({'id':'url','label':'رابط غير موثّق','type':'url','verification':'unknown'})
        edges.append({'source':'message','target':'url','type':'contains'})
    if asking_sensitive:
        nodes.append({'id':'action','label':'إجراء حساس مطلوب','type':'action'})
        edges.append({'source':'message','target':'action','type':'requests'})
    if transfer:
        edges.append({'source':'claim','target':'action','type':'unsupported_justification'})
    advice = ['تحقق من الجهة عبر موقعها الرسمي الذي تكتبه بنفسك، وليس من رابط الرسالة.'] if status in ('warning','caution','insufficient') else ['غياب المؤشرات لا يثبت أن الرسالة آمنة.']
    if asking_sensitive and any(d['type'] in ('otp_disclosure','password_disclosure') for d in detected):
        advice.insert(0, 'لا تشارك رمز التحقق أو كلمة المرور مع أي شخص.')
    return {
        'analysis_id':str(uuid.uuid4()),'status':status,'title':title,
        'risk_score':score,'risk_score_type':'heuristic_not_probability',
        'verified_facts':[],
        'unknown_claims':['شرعية الادعاء أو الصفة الرسمية لم يتم التحقق منها'] if authority else [],
        'urls_detected':urls, 'sensitive_actions':[{'type':d['type'],'explanation':d['explanation']} for d in detected] if asking_sensitive else [],
        'trust_transfers':[{'from':'claim','to':'action','relation':'unsupported_justification','reason':'الادعاء لا يثبت شرعية الإجراء.'}] if transfer else [],
        'rules':rules,'graph':{'nodes':nodes,'edges':edges},'advice':advice,
        'limitations':['تحليل استدلالي للنص فقط؛ لا يتحقق من أخبار أو ملكية روابط أو هوية المرسل.','قد توجد أخطاء، خصوصًا في النفي والصياغات غير المألوفة.','النتيجة ليست حكمًا نهائيًا أو احتمالًا مُعايرًا.']
    }
