import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

@st.cache_data
def load_data():
    df = pd.read_excel('result.xlsx')
    df.columns = [str(col).strip() for col in df.columns]
    return df

df = load_data()

LOGO_URL = "https://raw.githubusercontent.com/mohamedabdalatef71-jpg/result_app/ff737f289e52d0456b3202bf07a2d512ebb33d92/logo.jpg"

if LOGO_URL:
    logo_img_tag = f'<img src="{LOGO_URL}" style="max-height: 75px; margin-bottom: 5px; display: block; margin-right: 0; margin-left: auto; mix-blend-mode: multiply;" alt="شعار الكلية">'
else:
    logo_img_tag = '<div style="font-size: 35px; color: #1b4d3e; margin-bottom: 5px;">🏛️</div>'

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }
    .main-title { font-family: 'Amiri', serif; text-align: center; color: #2e8b57; font-size: 38px; font-weight: bold; margin-bottom: 0px; text-shadow: 1px 1px 3px rgba(0,0,0,0.5); }
    .sub-title { text-align: center; color: #d4af37; font-size: 22px; font-weight: bold; margin-bottom: 20px; }
    div.stTextInput > label { color: #d4af37 !important; font-weight: bold; font-size: 20px; text-align: center; display: block; }
    div.stTextInput input { border: 2px solid #d4af37; border-radius: 8px; text-align: center; font-size: 18px; background-color: #ffffff !important; color: #000000 !important; }
    div.stButton > button:first-child { background-color: #1b4d3e; color: white; font-size: 18px; font-weight: bold; border-radius: 8px; border: 2px solid #d4af37; width: 100%; transition: 0.3s; }
    div.stButton > button:first-child:hover { background-color: #14382d; color: #ffd700; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>نتيجة الفرقة الإعدادية</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='sub-title'>الترم الاول 2026</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    seat_no = st.text_input("ادخل رقم الجلوس:")
    show_button = st.button("إظهار النتيجة", use_container_width=True)
    st.markdown("<p style='text-align: center; color: #2e8b57; font-family: Amiri, serif; font-weight: bold; font-size: 19px; margin-top: 15px;'>قل لن يصيبنا إلا ما كتب الله لنا</p>", unsafe_allow_html=True)

if show_button:
    if seat_no:
        seat_col = "رقم الجلوس"
        if seat_col in df.columns:
            clean_input = str(seat_no).strip()
            df[seat_col] = df[seat_col].astype(str).str.strip().str.replace('.0', '', regex=False)
            match_indices = df.index[df[seat_col] == clean_input].tolist()
            
            if match_indices:
                st.success("تم العثور على النتيجة بنجاح!")
                idx = match_indices[0]
                row1 = df.iloc[idx]
                row2 = df.iloc[idx + 1] if (idx + 1) < len(df) else None
                
                student_data = {}
                for col in df.columns:
                    v1 = str(row1[col]).strip() if pd.notna(row1[col]) else ""
                    if v1.lower() == 'nan': v1 = ""
                    v2 = str(row2[col]).strip() if row2 is not None and pd.notna(row2[col]) else ""
                    if v2.lower() == 'nan': v2 = ""
                    
                    if col in ["كود الطالب", "رقم الجلوس"]:
                        combined = f"{v1}{v2}".strip()
                    else:
                        combined = f"{v1} {v2}".strip() if v1 and v2 and v1 != v2 else (v1 or v2)
                    student_data[col] = combined
                
                base_keys = ["رقم الجلوس", "اسم الطالب", "كود الطالب"]
                personal_info = {k: student_data.get(k, "") for k in base_keys if k in student_data or k in df.columns}
                subjects_info = {k: v for k, v in student_data.items() if k not in base_keys and k != seat_col}
                
                rows_html = "".join([f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in personal_info.items() if k])
                rows_html += '<tr><th style="background-color: #1b4d3e; color: white; text-align: right; padding: 10px 12px; white-space: nowrap;">المواد</th><th style="background-color: #1b4d3e; color: white; text-align: right; padding: 10px 12px; border-right: 2px solid #b8860b;">التقديرات / الدرجات</th></tr>'
                rows_html += "".join([f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in subjects_info.items() if k])

                full_card_html = f"""
                <!DOCTYPE html>
                <html lang="ar" dir="rtl">
                <head>
                    <meta charset="UTF-8">
                    <link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;700&display=swap" rel="stylesheet">
                    <style>
                        body {{ font-family: 'Cairo', sans-serif; background-color: #ffffff; margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; }}
                        .print-page-wrapper {{ 
                            border: 3px solid #1b4d3e; 
                            border-radius: 12px;
                            padding: 15px; 
                            width: 100%; 
                            max-width: 580px; 
                            background-color: #ffffff; 
                            position: relative; 
                            text-align: center; 
                            box-sizing: border-box;
                            overflow: hidden;
                        }}
                        .print-header-title {{ font-family: 'Amiri', serif; text-align: center; color: #2e8b57; font-size: 24px; font-weight: bold; margin-bottom: 0px; position: relative; z-index: 2; }}
                        .print-header-subtitle {{ text-align: center; color: #d4af37; font-size: 16px; font-weight: bold; margin-bottom: 4px; position: relative; z-index: 2; }}
                        .print-ayah {{ text-align: center; color: #2e8b57; font-family: 'Amiri', serif; font-weight: bold; font-size: 14px; margin-bottom: 8px; position: relative; z-index: 2; }}
                        .table-container {{ width: 100%; display: flex; justify-content: center; margin-bottom: 8px; position: relative; z-index: 2; }}
                        .styled-table {{ direction: rtl; border-collapse: separate; border-spacing: 0; font-size: 14px; background-color: rgba(255, 255, 255, 0.95); color: #000000; border: 2px solid #1b4d3e; border-radius: 8px; overflow: hidden; width: 100%; }}
                        .styled-table th {{ background-color: #1b4d3e; color: #ffffff; padding: 8px 10px; font-size: 15px; border-bottom: 2px solid #1b4d3e; border-right: 2px solid #b8860b; }}
                        .styled-table th:first-child {{ border-right: none; }}
                        .styled-table td {{ padding: 6px 10px; border-bottom: 1px solid #e0e0e0; border-right: 2px solid #1b4d3e; color: #000000; font-weight: bold; }}
                        .styled-table tr td:first-child {{ border-right: none; }}
                        .styled-table td:nth-child(1), .styled-table th:nth-child(1) {{ text-align: right; width: 45%; white-space: nowrap; }}
                        .styled-table td:nth-child(2), .styled-table th:nth-child(2) {{ text-align: right; width: 55%; }}
                        .styled-table tbody tr:nth-of-type(even) {{ background-color: rgba(250, 249, 246, 0.95); }}
                        
                        /* منطقة آية الكرسي في الفراغ تحت الجدول */
                        . kursi-text {{
                            font-family: 'Amiri', serif;
                            font-size: 11.5px;
                            color: #1b4d3e;
                            text-align: justify;
                            text-align-last: center;
                            line-height: 1.5;
                            margin: 8px 5px;
                            font-weight: bold;
                            position: relative;
                            z-index: 2;
                            opacity: 0.85;
                        }}

                        /* اسم الكلية وحقوق التصميم في الحافة تحت */
                        .footer-container {{
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                            margin-top: 8px;
                            border-top: 1px dashed #d4af37;
                            padding-top: 6px;
                            position: relative;
                            z-index: 2;
                        }}
                        .college-name {{ font-family: 'Amiri', serif; font-size: 13px; font-weight: bold; color: #d4af37; }}
                        .designer-credit {{ font-size: 11px; font-weight: bold; color: #2e8b57; }}
                        
                        /* العلامة المائية في منتصف الجدول وبشفافية هادئة وأمام العناصر */
                        .watermark-logo {{ 
                            position: absolute; 
                            top: 52%; 
                            left: 50%; 
                            transform: translate(-50%, -50%); 
                            width: 350px; 
                            opacity: 0.07; 
                            z-index: 10; 
                            pointer-events: none; 
                            mix-blend-mode: multiply;
                            filter: contrast(140%) brightness(105%);
                        }}
                        
                        .print-btn-container {{ margin-top: 20px; text-align: center; width: 100%; }}
                        .print-btn {{
                            background-color: #2e8b57; color: white; padding: 12px 40px; 
                            border: 2px solid #d4af37; border-radius: 8px; cursor: pointer; 
                            font-size: 18px; font-weight: bold; font-family: 'Cairo', sans-serif;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        }}
                        .print-btn:hover {{ background-color: #246d43; }}

                        @media print {{
                            @page {{
                                size: A4 portrait;
                                margin: 8mm;
                            }}
                            body {{ background-color: #ffffff; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                            .print-btn-container {{ display: none !important; }}
                            .print-page-wrapper {{ 
                                border: 3px solid #1b4d3e !important; 
                                width: 100% !important; 
                                max-width: 100% !important; 
                                box-shadow: none !important;
                                margin: 0 !important;
                            }}
                            .watermark-logo {{ 
                                opacity: 0.07 !important; 
                                z-index: 10 !important;
                                mix-blend-mode: multiply !important;
                                -webkit-print-color-adjust: exact; 
                                print-color-adjust: exact; 
                            }}
                            .styled-table th {{ background-color: #1b4d3e !important; color: #ffffff !important; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="print-page-wrapper">
                        <!-- العلامة المائية في منتصف الجدول تماماً -->
                        <img src="{LOGO_URL}" class="watermark-logo" alt="Watermark">
                        
                        <div style="margin-bottom: 2px; text-align: right; position: relative; z-index: 2;">{logo_img_tag}</div>
                        <div class="print-header-title">نتيجة الفرقة الإعدادية</div>
                        <div class="print-header-subtitle">الترم الاول 2026</div>
                        <div class="print-ayah">قل لن يصيبنا إلا ما كتب الله لنا</div>
                        
                        <div class="table-container">
                            <table class='styled-table'>
                                <thead><tr><th>بيانات الطالب</th><th>النتيجة</th></tr></thead>
                                <tbody>{rows_html}</tbody>
                            </table>
                        </div>

                        <!-- آية الكرسي كاملة في المنطقة الخالية تحت الجدول -->
                        <div class="kursi-text">
                            اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ ما فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ ۖ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ
                        </div>

                        <!-- حافة الصفحة من تحت: اسم الكلية واسمك بخط مزخرف متناسق -->
                        <div class="footer-container">
                            <div class="college-name">كلية الهندسة - جامعة الأزهر</div>
                            <div class="designer-credit">Designed by Eng. Mohamed Abdelatif</div>
                        </div>
                    </div>
                    
                    <div class="print-btn-container">
                        <button class="print-btn" onclick="window.print();">🖨️ طباعة النتيجة</button>
                    </div>
                </body>
                </html>
                """
                components.html(full_card_html, height=750, scrolling=True)
            else:
                st.error("رقم الجلوس غير موجود، تأكد من الرقم وادخله مرة أخرى.")
        else:
            st.error("عفواً، عمود 'رقم الجلوس' غير متطابق في ملف الإكسيل.")
    else:
        st.warning("الرجاء إدخال رقم الجلوس أولاً.")
