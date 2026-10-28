from backend.engine.analyzer import analyze
from backend.engine.explain import build_report

def test_report_has_method_and_explanation():
    result=build_report(analyze('مؤسسة رسمية ولهيك ادخل رمز التحقق OTP'), 'example')
    assert result['analysis_method']=='deterministic_rules'
    assert result['verification_performed'] is False
    assert result['educational_explanations']

def test_no_independent_verification_claim():
    result=build_report(analyze('الموقع الرسمي https://example.invalid/verify'),'example')
    assert result['verified_facts']==[]

def test_does_not_execute_untrusted_input():
    result=analyze('<script>alert(1)</script>')
    assert result['risk_score']==0

def test_neutralized_warning():
    result=analyze('إياك تشارك كلمة المرور مع أي شخص')
    assert result['risk_score']==0
