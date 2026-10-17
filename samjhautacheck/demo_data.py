"""Demo contracts and pre-computed forensic audits for SamjhautaCheck.
Features a realistic, predatory Bangalore/Mumbai 11-month rental agreement.
"""

from samjhautacheck.models import AuditReport, RedFlag

DEMO_RENTAL_AGREEMENT = """RESIDENTIAL LEASE AND TENANCY AGREEMENT

THIS LEASE AGREEMENT is entered into at Bengaluru on this 1st day of November 2024, BY AND BETWEEN:
Mr. R. K. Hegde, residing at Indiranagar, Bengaluru - 560038, hereinafter referred to as the "LESSOR / LANDLORD" (which expression shall unless repugnant to the context include his heirs, executors, and assigns) of the ONE PART;

AND
Mr. Rahul Sharma, employed at HSR Layout, Bengaluru - 560102, hereinafter referred to as the "LESSEE / TENANT" (which expression shall unless repugnant to the context include his heirs and permitted assigns) of the OTHER PART.

WHEREAS the Lessor is the absolute owner of Flat No. 402, Pinecrest Apartments, Sarjapur Road, Bengaluru (hereinafter called the "Schedule Premises").

NOW THIS AGREEMENT WITNESSETH AS FOLLOWS:

1. TERM OF LEASE:
The lease shall be for an initial period of 11 (Eleven) months commencing from 1st November 2024.

2. MONTHLY RENT:
The Tenant agrees to pay a monthly rent of Rs. 45,000/- (Rupees Forty-Five Thousand only) payable on or before the 5th day of each English calendar month. Late payment shall attract a daily penalty of Rs. 1,000/-.

3. UNILATERAL RENT ESCALATION:
Upon completion of the initial 11 months, the monthly rent shall automatically escalate by 15% (Fifteen Percent) for the subsequent term, irrespective of prevailing market rates or tenant negotiation.

4. INTEREST-FREE SECURITY DEPOSIT & FORFEITURE:
The Tenant has deposited an interest-free refundable security deposit of Rs. 4,50,000/- (Rupees Four Lakhs Fifty Thousand only, equivalent to 10 months rent). It is strictly agreed that should the Tenant vacate the premises before completing the 11-month term for any reason whatsoever, the entire security deposit of Rs. 4,50,000/- shall be forfeited unconditionally to the Landlord as liquidated damages.

5. ARBITRARY PAINTING & CLEANING DEDUCTIONS:
Upon vacating the Schedule Premises, irrespective of duration of stay or actual condition of walls and fixtures, a flat non-negotiable deduction of Rs. 50,000/- plus 1 (One) month's full rent shall be deducted from the security deposit towards professional painting, deep cleaning, and wear-and-tear damages.

6. STRUCTURAL REPAIRS & MAINTENANCE BURDEN:
The Tenant shall be solely liable for all repair works, plumbing leakages, seepage, sanitary replacements, and electrical repairs exceeding Rs. 500/-, including internal seepage or dampness issues arising during tenancy.

7. UNRESTRICTED RIGHT OF ENTRY WITHOUT NOTICE:
The Landlord or his authorized representatives, family members, or prospective buyers reserve the absolute right to enter and inspect the Schedule Premises at any hour of the day or night without requiring prior oral or written notice or consent from the Tenant.

8. LOCK-IN PERIOD & ASYMMETRIC TERMINATION:
The Tenant is bound by a strict 6-month lock-in period during which tenant notice to vacate is invalid and rent for remaining months remains payable. However, the Landlord reserves the unilateral right to terminate this tenancy and demand immediate vacation within 48 (Forty-Eight) hours without assigning any cause.

9. REFUND OF SECURITY DEPOSIT TIMELINE:
The remaining balance of the Security Deposit, after all deductions and repairs determined solely at the Landlord's discretion, shall be refunded to the Tenant within 90 (Ninety) days following physical handover of vacant possession. No interest or compensation shall accrue to the Tenant for delayed refund.

10. RESTRICTIONS ON GUESTS:
No visitors, friends, or overnight guests of the opposite gender or non-immediate family are permitted inside the premises without prior written approval from the Landlord.

IN WITNESS WHEREOF, the parties hereto have set their hands on the day and year first written above.

LESSOR / LANDLORD: ____________________
LESSEE / TENANT:   ____________________
WITNESS 1:         ____________________
WITNESS 2:         ____________________
"""

DEMO_AUDIT_REPORT = AuditReport(
    document_type="11-Month Residential Rental Agreement (Karnataka / Bangalore)",
    fairness_score=24,
    summary=(
        "Extremely one-sided and predatory tenancy agreement containing severe financial traps, "
        "grossly asymmetric termination clauses, unrestricted privacy violations, and unauthorized "
        "penalties that contradict standard Model Tenancy Act principles and Indian contract law."
    ),
    key_takeaways=[
        "10-month deposit (₹4.5L) subject to total forfeiture for early exit and arbitrary ₹95k+ deductions.",
        "Unrestricted 24/7 landlord entry violates basic constitutional and common law tenant privacy rights.",
        "Asymmetric lock-in: Landlord can evict in 48 hours; Tenant faces 6-month lock-in and complete deposit loss.",
        "Mandatory 15% annual rent hike is double the standard Bangalore market rate (5-7%).",
        "90-day deposit refund timeline leaves ₹3.5L+ trapped for 3 months with zero interest.",
    ],
    red_flags=[
        RedFlag(
            clause_quote=(
                "Clause 4: 'should the Tenant vacate the premises before completing the 11-month term "
                "for any reason whatsoever, the entire security deposit of Rs. 4,50,000/- shall be forfeited unconditionally'"
            ),
            plain_english_risk=(
                "Total confiscation of 10 months' rent (₹4.5 Lakhs) if you have a job transfer, family emergency, "
                "or medical need to move out early. Indian courts have repeatedly held unreasonable liquidated "
                "damage forfeitures to be void under Section 74 of the Indian Contract Act."
            ),
            severity_level="Critical",
            counter_proposal_text=(
                "Either party may terminate this agreement by providing 1 (One) month prior written notice. "
                "Upon completion of notice period, the security deposit shall be fully refunded subject only to "
                "actual unpaid rent and verified physical damage."
            ),
        ),
        RedFlag(
            clause_quote=(
                "Clause 5: 'irrespective of duration of stay or actual condition of walls and fixtures, a flat non-negotiable "
                "deduction of Rs. 50,000/- plus 1 (One) month's full rent shall be deducted from the security deposit towards professional painting'"
            ),
            plain_english_risk=(
                "Guaranteed loss of ₹95,000 on day one of move-out. A standard painting charge in Bangalore "
                "is capped at 1 month rent or actual vendor receipt (₹15k-₹25k) and only applies for stays over 11 months."
            ),
            severity_level="Critical",
            counter_proposal_text=(
                "Painting charges upon handover shall be limited to actual quotation from a mutual vendor, "
                "capped at a maximum of Rs. 20,000/-, and applicable only if the tenancy extends beyond 11 months."
            ),
        ),
        RedFlag(
            clause_quote=(
                "Clause 7: 'reserve the absolute right to enter and inspect the Schedule Premises at any hour "
                "of the day or night without requiring prior oral or written notice or consent'"
            ),
            plain_english_risk=(
                "Complete loss of privacy and security. Anyone representing the landlord could walk in while you "
                "are sleeping or away without warning. This violates the legal covenant of quiet enjoyment."
            ),
            severity_level="Critical",
            counter_proposal_text=(
                "The Landlord or their authorized agent may inspect the premises only between 10:00 AM and 6:00 PM "
                "after giving at least 24 hours prior written notice via WhatsApp/Email, in the presence of the Tenant."
            ),
        ),
        RedFlag(
            clause_quote=(
                "Clause 8: 'Tenant is bound by a strict 6-month lock-in period... However, the Landlord reserves the "
                "unilateral right to terminate this tenancy and demand immediate vacation within 48 (Forty-Eight) hours'"
            ),
            plain_english_risk=(
                "Extreme asymmetry. You could be rendered homeless in 2 days with zero recourse, while you are legally "
                "shackled for 6 months. A fair lease demands mutual 1-month or 2-month notice."
            ),
            severity_level="High",
            counter_proposal_text=(
                "Both Landlord and Tenant shall be bound by a mutual 30-day notice period for termination. "
                "Neither party shall have unilateral right of immediate eviction without cause."
            ),
        ),
        RedFlag(
            clause_quote=(
                "Clause 3: 'monthly rent shall automatically escalate by 15% (Fifteen Percent) for the subsequent term, "
                "irrespective of prevailing market rates'"
            ),
            plain_english_risk=(
                "A 15% hike compound raises your rent from ₹45,000 to ₹51,750 next year. Standard escalation in "
                "residential leases across metro India is 5% to 8% maximum."
            ),
            severity_level="High",
            counter_proposal_text=(
                "Renewal for any subsequent term shall be mutually agreed upon with rent escalation capped at "
                "5% to 7% subject to mutual consent."
            ),
        ),
        RedFlag(
            clause_quote=(
                "Clause 9: 'remaining balance of the Security Deposit... shall be refunded to the Tenant within 90 (Ninety) days'"
            ),
            plain_english_risk=(
                "Your ₹3.5L+ capital remains locked for 3 months after you've surrendered keys, leaving you unable to pay "
                "the deposit for your next home. Standard practice is refund on the day of key handover."
            ),
            severity_level="High",
            counter_proposal_text=(
                "The Security Deposit, less undisputed deductions, shall be refunded by NEFT/RTGS on the exact day "
                "of vacating and key handover. Delays beyond 7 days shall accrue interest at 12% per annum."
            ),
        ),
        RedFlag(
            clause_quote=(
                "Clause 6: 'Tenant shall be solely liable for all repair works, plumbing leakages, seepage, "
                "sanitary replacements... exceeding Rs. 500'"
            ),
            plain_english_risk=(
                "Shifts landlord's structural liabilities onto you. Building seepage, pipe burst, or water tank "
                "leakage can easily cost ₹30,000 - ₹80,000, which is structurally the landlord's duty."
            ),
            severity_level="Medium",
            counter_proposal_text=(
                "Tenant is responsible for minor consumable maintenance (bulbs, washers) up to Rs. 1,000. "
                "All major plumbing, electrical, dampness, and structural repairs are the Landlord's sole responsibility."
            ),
        ),
    ],
    missing_protections=[
        "No clause requiring the Landlord to return the security deposit on the date of key handover.",
        "No interest penalty clause on the Landlord for delayed deposit return (standard is 8-12% p.a.).",
        "Missing clear distinction between structural repairs (Landlord responsibility) vs minor wear (Tenant).",
        "No Force Majeure or job relocation clause permitting early exit without deposit forfeiture.",
        "No dispute resolution / mediation mechanism before court litigation.",
        "Missing clause confirming landlord's clear title, property tax clearance, and right to let the property.",
    ],
    whatsapp_negotiation_draft=(
        "Dear Mr. Hegde, Good day! Thank you for sharing the draft rental agreement for Flat 402, Pinecrest Apartments. "
        "We are really excited to make this our home and appreciate your support. "
        "\n\nI reviewed the draft with our legal counsel and noticed a few standard clauses that seem unintentionally one-sided. "
        "To ensure a smooth, long-term tenancy for both of us, could we kindly adjust the following 3 points before signing?\n\n"
        "1. Notice & Termination: A mutual 1-month notice period for both of us, rather than the 48-hour eviction clause and full deposit forfeiture.\n"
        "2. Painting & Move-out Deduction: Align with standard Bangalore practice—either actual receipts capped at ₹20k or 1 month rent (instead of both ₹50k + 1 month rent).\n"
        "3. Deposit Refund: Refund of deposit on the day of key handover upon mutual inspection, rather than 90 days later.\n\n"
        "These align with the standard Model Tenancy guidelines and will give us both peace of mind. "
        "I'm ready to transfer the remaining deposit and sign once updated. Thank you so much for understanding!"
    ),
    spoken_briefing_script=(
        "Listen to me very carefully before you sign this agreement. This contract has massive financial traps. "
        "First, if you have an emergency or job transfer and move out before 11 months, the landlord gets to keep your entire 4.5 lakh deposit. "
        "Second, they have written an automatic 95,000 rupee deduction for painting when you leave, even if the walls are spotless! "
        "Third, the landlord gave himself permission to walk into your flat at midnight without notice, but can evict you in just 48 hours. "
        "Do not sign this draft as-is. Copy the negotiation message we generated, send it on WhatsApp, and ask for a mutual 1-month notice and immediate deposit refund."
    ),
)

# Regional translations for the spoken briefing script
REGIONAL_BRIEFING_SCRIPTS = {
    "en": DEMO_AUDIT_REPORT.spoken_briefing_script,
    "hi": (
        "इस समझौते पर हस्ताक्षर करने से पहले मेरी बात बहुत ध्यान से सुनिए। इस अनुबंध में भारी वित्तीय जाल बिछे हुए हैं। "
        "पहली बात, अगर आपकी नौकरी बदलती है या कोई आपात स्थिति आती है और आप 11 महीने से पहले फ्लैट खाली करते हैं, तो मकान मालिक आपकी पूरी साढ़े चार लाख की सुरक्षा राशि जब्त कर लेगा। "
        "दूसरी बात, बाहर निकलते समय पेंटिंग के नाम पर 95,000 रुपये की मनमानी कटौती जोड़ी गई है। "
        "तीसरी बात, मकान मालिक बिना किसी पूर्व सूचना के आधी रात को भी आपके फ्लैट में आने का अधिकार रखता है, जबकि आपको केवल 48 घंटे में बाहर निकाल सकता है। "
        "इस मसौदे पर ऐसे ही हस्ताक्षर मत कीजिए। हमारा तैयार किया गया व्हाट्सऐप संदेश भेजकर इसे तुरंत ठीक करवाएं।"
    ),
    "hinglish": (
        "Bhai, ye contract sign karne se pehle meri baat dhyan se sun lo. Isme bohot bade financial traps hain. "
        "Pehla, agar job transfer ya emergency ki wajah se tumne 11 months se pehle flat chhoda, toh landlord tumhara pura 4.5 lakh deposit forfeit kar lega! "
        "Doosra, move-out pe 95,000 rupees ka flat painting deduction daal rakha hai, chahe walls ekdum new hon. "
        "Aur sabse dangerous: Landlord bina notice ke kisi bhi waqt flat me ghus sakta hai, par tumhe 48 hours me nikaal sakta hai. "
        "Isko as-is bilkul sign mat karo. Humne jo WhatsApp draft banaya hai, use copy karo aur landlord ko send karke mutual 1-month notice insist karo."
    ),
    "te": (
        "ఈ అద్దె ఒప్పందంపై సంతకం చేసే ముందు నా మాట జాగ్రత్తగా వినండి. ఇందులో చాలా పెద్ద ఆర్థిక ప్రమాదాలు దాగి ఉన్నాయి. "
        "మొదటిది, ఏదైనా అత్యవసర పరిస్థితి వల్ల మీరు 11 నెలల కంటే ముందే ఇల్లు ఖాళీ చేస్తే, మీ రూ. 4.5 లక్షల డిపాజిట్ మొత్తాన్ని ఓనర్ జప్తు చేసుకుంటారు. "
        "రెండవది, మీరు ఖాళీ చేసేటప్పుడు పెయింటింగ్ కోసం రూ. 95,000 అన్యాయంగా కట్ చేస్తామని రాశారు. "
        "మూడవది, ఎటువంటి ముందస్తు సమాచారం లేకుండా ఎప్పుడైనా మీ ఫ్లాట్‌లోకి వచ్చే అధికారాన్ని ఓనర్ ఉంచుకున్నారు, కానీ మిమ్మల్ని 48 గంటల్లో ఖాళీ చేయించవచ్చు. "
        "ఈ ఒప్పందంపై ఇప్పుడే సంతకం చేయవద్దు. మేము సిద్ధం చేసిన వాట్సాప్ మెసేజ్‌ని పంపించి నిబంధనలను సవరించమని అడగండి."
    ),
    "ta": (
        "இந்த வாடகை ஒப்பந்தத்தில் கையெழுத்திடுவதற்கு முன் நான் சொல்வதை கவனமாகக் கேளுங்கள். இதில் கடுமையான நிதி அபாயங்கள் உள்ளன. "
        "முதலாவதாக, 11 மாதங்களுக்கு முன் நீங்கள் வீட்டை காலி செய்தால், உங்களின் 4.5 லட்சம் ரூபாய் முழு முன்பணத்தையும் வீட்டு உரிமையாளர் பறிமுதல் செய்துவிடுவார். "
        "இரண்டாவதாக, நீங்கள் வெளியேறும்போது வர்ணம் பூசுவதற்காக ரூ. 95,000 கட்டாயமாக பிடித்தம் செய்யப்படும் என்று எழுதப்பட்டுள்ளது. "
        "மூன்றாவதாக, எந்த முன்னறிவிப்பும் இன்றி எந்த நேரத்திலும் உங்கள் வீட்டிற்குள் நுழைய உரிமையாளருக்கு அதிகாரம் உள்ளது, ஆனால் உங்களை 48 மணிநேரத்தில் வெளியேற்ற முடியும். "
        "இதை அப்படியே கையெழுத்திடாதீர்கள். நாங்கள் உருவாக்கியுள்ள வாட்ஸ்அப் செய்தியை அனுப்பி திருத்தங்களை உடனே கோருங்கள்."
    ),
}
