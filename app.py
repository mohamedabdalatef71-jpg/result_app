import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

@st.cache_data
def load_data():
    xls = pd.ExcelFile('result.xlsx')
    sheet_name = xls.sheet_names[0]
    df = pd.read_excel(xls, sheet_name=sheet_name)
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
        possible_cols = [c for c in df.columns if 'جلوس' in str(c) or str(c).strip() in ['الجلوس', 'رقم الجلوس', 'رقم_الجلوس']]
        seat_col = possible_cols[0] if possible_cols else None
        
        if seat_col:
            clean_input = str(seat_no).strip()
            df[seat_col] = df[seat_col].astype(str).str.strip().str.replace('.0', '', regex=False)
            match_indices = df.index[df[seat_col] == clean_input].tolist()
            
            if match_indices:
                st.success("تم العثور على النتيجة بنجاح!")
                idx = match_indices[0]
                row = df.iloc[idx]
                
                student_data = {}
                for col in df.columns:
                    val = str(row[col]).strip() if pd.notna(row[col]) else ""
                    if val.lower() == 'nan': 
                        val = ""
                    else:
                        val = val.replace('.0', '') if val.endswith('.0') and val.replace('.', '', 1).isdigit() else val
                    student_data[col] = val
                
                # البحث عن المفاتيح الأساسية بدقة
                seat_key = next((c for c in df.columns if 'جلوس' in str(c)), None)
                name_key = next((c for c in df.columns if 'اسم' in str(c) or 'إسم' in str(c) or 'طالب' in str(c)), None)
                grade_key = next((c for c in df.columns if 'التقدير' in str(c)), None)
                order_key = next((c for c in df.columns if 'الترتيب' in str(c)), None)
                # دالة دقيقة لتمييز عمود النتيجة (ناجح/راسب) عن اسم الجدول
                status_key = next((c for c in df.columns if str(c).strip() == 'النتيجة'), None)
                total_key = next((c for c in df.columns if 'المجموع' in str(c) or 'النسبة' in str(c)), None)
                
                ordered_personal_keys = []
                for k in [seat_key, name_key, grade_key, order_key, status_key, total_key]:
                    if k and k in student_data and k not in ordered_personal_keys:
                        ordered_personal_keys.append(k)
                
                # التقاط أي أعمدة أساسية إضافية مفقودة
                for k in df.columns:
                    if any(x in str(k) for x in ['جلوس', 'اسم', 'إسم', 'طالب', 'كود', 'التقدير', 'الترتيب', 'المجموع', 'النسبة']) or str(k).strip() == 'النتيجة':
                        if k not in ordered_personal_keys:
                            ordered_personal_keys.append(k)

                personal_info = {k: student_data[k] for k in ordered_personal_keys if k in student_data and student_data[k] != ""}
                
                # المواد فقط (استبعاد الأعمدة الأساسية المحددة فقط لعدم تكرارها)
                excluded_keys = set(ordered_personal_keys)
                subjects_info = {k: v for k, v in student_data.items() if k not in excluded_keys and v != ""}
                
                rows_html = "".join([f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in personal_info.items()])
                rows_html += '<tr><th style="background-color: #1b4d3e; color: white; text-align: right; padding: 10px 12px; white-space: nowrap;">المواد</th><th style="background-color: #1b4d3e; color: white; text-align: right; padding: 10px 12px; border-right: 2px solid #b8860b;">التقديرات / الدرجات</th></tr>'
                rows_html += "".join([f"<tr><td><b>{k}</b></td><td>{v}</td></tr>" for k, v in subjects_info.items()])

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
                        
                        .kursi-text {{
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
                    </style>
                </head>
                <body>
                    <div class="print-page-wrapper">
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

                        <div class="kursi-text">
                            اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ ۚ لَا تَأْخُذُهُ سِنَةٌ وَلَا نَوْمٌ ۚ لَّهُ ما فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ ۗ مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ ۚ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ ۖ وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ ۚ وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَلَا يَئُودُهُ حِفْظُهُمَا ۚ وَهُوَ الْعَلِيُّ الْعَظِيمُ
                        </div>

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
            st.error("عفواً، لم يتم العثور على عمود رقم الجلوس.")
    else:
        st.warning("الرجاء إدخال رقم الجلوس أولاً.")
