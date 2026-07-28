import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

@st.cache_data
def load_data():
    df = pd.read_excel('result.xlsx')
    df.columns = [str(col).strip() for col in df.columns]
    return df

df = load_data()

# تصميم أكاديمي وتنسيق صفحة الطباعة والإطار الفخم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@700&family=Cairo:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
    }

    .main-title {
        font-family: 'Amiri', serif;
        text-align: center;
        color: #2e8b57;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 0px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }
    
    .sub-title {
        text-align: center;
        color: #d4af37;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    div.stTextInput > label {
        color: #d4af37 !important;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        display: block;
    }
    div.stTextInput input {
        border: 2px solid #d4af37;
        border-radius: 8px;
        text-align: center;
        font-size: 18px;
        background-color: #ffffff !important; 
        color: #000000 !important;
    }
    
    div.stButton > button:first-child {
        background-color: #1b4d3e;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: 2px solid #d4af37;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #14382d;
        color: #ffd700;
    }
    
    .table-container {
        width: 100%;
        overflow-x: auto;
        display: flex;
        justify-content: center;
        margin-top: 15px;
        margin-bottom: 15px;
        padding-bottom: 5px;
    }
    
    .styled-table {
        direction: rtl;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 16px;
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #1b4d3e;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(27, 77, 62, 0.3);
        width: 100%;
        max-width: 600px;
        min-width: 450px;
    }
    
    .styled-table th {
        background-color: #1b4d3e;
        color: #ffffff;
        padding: 12px 15px;
        font-size: 18px;
        border-bottom: 2px solid #1b4d3e;
        border-right: 2px solid #b8860b;
    }
    .styled-table th:first-child {
        border-right: none;
    }
    
    .styled-table td {
        padding: 10px 15px;
        border-bottom: 1px solid #e0e0e0;
        border-right: 2px solid #1b4d3e;
        color: #000000;
        font-weight: bold;
    }
    .styled-table tr td:first-child {
        border-right: none;
    }
    .styled-table tbody tr:last-child td {
        border-bottom: none;
    }
    
    .styled-table td:nth-child(1), .styled-table th:nth-child(1) { 
        text-align: right; 
        padding-right: 15px; 
        width: 45%;
        white-space: nowrap;
    }
    .styled-table td:nth-child(2), .styled-table th:nth-child(2) { 
        text-align: right; 
        padding-right: 20px; 
        width: 55%;
    }
    
    .styled-table tbody tr:nth-of-type(even) { background-color: #faf9f6; }
    .styled-table tbody tr:nth-of-type(odd) { background-color: #ffffff; }

    .designer-credit {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        color: #2e8b57;
        margin-top: 8px;
        margin-bottom: 15px;
        width: 100%;
    }

    /* إعدادات البرواز وإخفاء العناصر عند الطباعة */
    @media print {
        body { 
            background: white !important; 
            margin: 0 !important;
            padding: 0 !important;
        }
        
        .stButton, .stTextInput, h1, h3, hr, div[data-testid="stSidebar"], div[data-testid="stSuccess"] {
            display: none !important;
        }
        
        .print-page-wrapper {
            border: 4px solid #1b4d3e !important;
            border-radius: 15px !important;
            padding: 20px !important;
            margin: 5px auto !important;
            max-width: 700px !important;
            background-color: #ffffff !important;
            box-shadow: none !important;
        }
        
        .print-header-title {
            font-family: 'Amiri', serif !important;
            text-align: center !important;
            color: #2e8b57 !important;
            font-size: 28px !important;
            font-weight: bold !important;
            display: block !important;
            margin-bottom: 0px !important;
        }
        
        .print-header-subtitle {
            text-align: center !important;
            color: #d4af37 !important;
            font-size: 18px !important;
            font-weight: bold !important;
            display: block !important;
            margin-bottom: 10px !important;
        }

        .print-ayah {
            text-align: center !important;
            color: #2e8b57 !important;
            font-family: 'Amiri', serif !important;
            font-weight: bold !important;
            font-size: 15px !important;
            display: block !important;
            margin-bottom: 15px !important;
        }

        .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 50px;
            color: rgba(27, 77, 62, 0.04);
            z-index: 9999;
            pointer-events: none;
            font-weight: bold;
            white-space: nowrap;
        }
    }
    </style>
""", unsafe_allow_html=True)

# العناوين في الموقع العادي
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
                
                if (idx + 1) < len(df):
                    row2 = df.iloc[idx + 1]
                else:
                    row2 = None
                
                student_data = {}
                for col in df.columns:
                    v1 = str(row1[col]).strip() if pd.notna(row1[col]) else ""
                    if v1.lower() == 'nan': v1 = ""
                    
                    v2 = ""
                    if row2 is not None:
                        v2 = str(row2[col]).strip() if pd.notna(row2[col]) else ""
                        if v2.lower() == 'nan': v2 = ""
                    
                    if col in ["كود الطالب", "رقم الجلوس"]:
                        combined = f"{v1}{v2}".strip()
                    else:
                        if v1 and v2 and v1 != v2:
                            combined = f"{v1} {v2}".strip()
                        elif v1:
                            combined = v1
                        elif v2:
                            combined = v2
                        else:
                            combined = ""
                            
                    student_data[col] = combined
                
                base_keys = ["رقم الجلوس", "اسم الطالب", "كود الطالب"]
                personal_info = {k: student_data.get(k, "") for k in base_keys if k in student_data or k in df.columns}
                subjects_info = {k: v for k, v in student_data.items() if k not in base_keys and k != seat_col}
                
                # بناء الجدول مع تفعيل العرض السليم بالـ HTML
                rows_html = ""
                for k, v in personal_info.items():
                    if k:
                        rows_html += f"<tr><td><b>{k}</b></td><td>{v}</td></tr>"
                
                rows_html += f"""
                    <tr>
                        <th style="background-color: #1b4d3e; color: white; text-align: right; padding: 12px 15px; white-space: nowrap;">المواد</th>
                        <th style="background-color: #1b4d3e; color: white; text-align: right; padding: 12px 15px; border-right: 2px solid #b8860b;">التقديرات / الدرجات</th>
                    </tr>
                """
                
                for k, v in subjects_info.items():
                    if k:
                        rows_html += f"<tr><td><b>{k}</b></td><td>{v}</td></tr>"

                # تجميع القالب كاملاً داخل الـ wrapper الخاص بالطباعة والبرواز
                complete_html = f"""
                <div class="print-page-wrapper">
                    <div class="watermark">نتيجة الفرقة الإعدادية - الترم الاول 2026</div>
                    <div class="print-header-title">نتيجة الفرقة الإعدادية</div>
                    <div class="print-header-subtitle">الترم الاول 2026</div>
                    <div class="print-ayah">قل لن يصيبنا إلا ما كتب الله لنا</div>
                    
                    <div class="table-container">
                        <table class='styled-table'>
                            <thead>
                                <tr>
                                    <th>بيانات الطالب</th>
                                    <th>النتيجة</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rows_html}
                            </tbody>
                        </table>
                    </div>
                    <div class="designer-credit">Designed by Engineer Mohamed Abdelatif Elsayed</div>
                </div>
                """
                
                st.markdown(complete_html, unsafe_allow_html=True)
                
                # زر الطباعة
                print_button_code = """
                <div style="text-align: center; margin-top: 15px;">
                    <button onclick="parent.window.print();" style="background-color: #2e8b57; color: white; padding: 12px 35px; border: 2px solid #d4af37; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-family: 'Cairo', sans-serif;">
                        🖨️ طباعة النتيجة
                    </button>
                </div>
                """
                components.html(print_button_code, height=70)
                
            else:
                st.error("رقم الجلوس غير موجود، تأكد من الرقم وادخله مرة أخرى.")
        else:
            st.error("عفواً، عمود 'رقم الجلوس' غير متطابق في ملف الإكسيل.")
    else:
        st.warning("الرجاء إدخال رقم الجلوس أولاً.")
