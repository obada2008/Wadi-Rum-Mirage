from backend.engine.analyzer import analyze

def test_detects_unsupported_trust_transfer():
    result = analyze('أعلنت مؤسسة رسمية عن خدمة جديدة، ولهيك ادخل رمز التحقق OTP')
    assert result['status'] == 'warning'
    assert result['trust_transfers']
    assert 'R05' in [r['id'] for r in result['rules']]

def test_warning_about_otp_not_scored_as_request():
    result = analyze('لا تبعت رمز التحقق لأي شخص حتى لو ادعى أنه موظف رسمي')
    assert not result['sensitive_actions']
    assert result['risk_score'] == 0

def test_plain_information_no_high_risk():
    result = analyze('تابع الموقع الرسمي للمؤسسة لمعرفة آخر الأخبار')
    assert result['status'] != 'warning'

def test_urgency_and_payment():
    result = analyze('ادفع رسوم التفعيل فورا حتى لا يتم إيقاف حسابك')
    assert result['risk_score'] > 0

def test_arabic_variant():
    result = analyze('لهذا أدخل رمز التحقق الآن لمؤسسة حكومية')
    assert result['trust_transfers']

def test_never_verifies_links():
    result = analyze('الجهة الرسمية: https://example.invalid/path')
    assert result['verified_facts'] == []
    assert result['urls_detected']

def test_rejects_long_input():
    import pytest
    with pytest.raises(ValueError):
        analyze('x'*5001)
