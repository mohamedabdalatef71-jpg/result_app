import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
  df = pd.read_excel('result.xlsx')
  df.columns = [str(col).strip() for col in df.columns]

  processed_rows = []
  for i in range(0, len(df) - 1, 2):
    row1 = df.iloc[i]
    row2 = df.iloc[i + 1]
    combined_row = {}
    for col in df.columns:
      val1 = str(row1[col]).strip() if pd.notna(row1[col]) else ''
      val2 = str(row2[col]).strip() if pd.notna(row2[col]) else ''

      parts = []
      for v in [val1, val2]:
        if v and v != 'nan' and v not in parts:
          parts.append(v)
      combined_row[col] = ' '.join(parts)
    processed_rows.append(combined_row)

  if len(df) % 2 != 0:
    last_row = {}
    for col in df.columns:
      v = str(df.iloc[-1][col]).strip() if pd.notna(df.iloc[-1][col]) else ''
      last_row[col] = '' if v == 'nan' else v
    processed_rows.append(last_row)

  return pd.DataFrame(processed_rows)


df = load_data()

# عنوان الموقع باللون الأزرق وفي المنتصف مع إضافة (الترم الاول 2026)
st.markdown(
    "<h1 style='text-align: center; color: #007BFF; margin-bottom:"
    " 5px;'>نتيجة الفرقة الإعدادية</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align: center; color: #555555; margin-bottom:"
    " 20px;'>الترم الاول 2026</h3>",
    unsafe_allow_html=True,
)

# التنسيق النهائي مع زيادة العرض بمقدار 2 سم تقريباً
st.markdown(
    """
    <style>
    div.stTextInput > label {
        color: #ff6600 !important;
        font-weight: bold;
        font-size: 18px;
        text-align: center;
        display: block;
    }
    div.stTextInput input {
        border: 2px solid #ff6600;
        border-radius: 8px;
        text-align: center;
        font-size: 16px;
    }
    
    div.stButton > button:first-child {
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
        color: white;
    }
    
    .table-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .styled-table {
        direction: rtl;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 16px;
        font-family: sans-serif;
        background-color: #ffffff;
        color: #000000;
        border: 2px solid #000000;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        width: auto;
        min-width: 530px; /* تم تكبير العرض الأدنى بمقدار 2 سم تقريباً */
        max-width: 680px; /* تم تكبير العرض الأقصى بمقدار 2 سم تقريباً */
    }
    
    .styled-table th {
        background-color: #007BFF;
        color: white;
        padding: 12px 15px;
        font-size: 18px;
        border-bottom: 2px solid #000000;
        border-right: 2px solid #000000;
    }
    .styled-table th:first-child {
        border-right: none;
    }
    
    .styled-table td {
        padding: 10px 15px;
        border-bottom: 2px solid #000000;
        border-right: 2px solid #000000;
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
    
    .styled-table tbody tr:nth-of-type(even) { background-color: #f9f9f9; }
    .styled-table tbody tr:nth-of-type(odd) { background-color: #ffffff; }

    .designer-credit {
        text-align: center;
        font-size: 14px;
        font-weight: bold;
        color: #555555;
        margin-top: 8px;
        margin-bottom: 15px;
    }

    @media print {
        body { background: white !important; }
        .stButton, .stTextInput, h1, h3, hr, div[data-testid="stSidebar"] {
            display: none !important;
        }
        .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 70px;
            color: rgba(0, 123, 255, 0.08);
            z-index: 9999;
            pointer-events: none;
            font-weight: bold;
            white-space: nowrap;
        }
    }
    </style>
""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  seat_no = st.text_input('ادخل رقم الجلوس:')
  show_button = st.button('إظهار النتيجة', use_container_width=True)

  st.markdown(
      "<p style='text-align: center; color: #ff6600; font-weight: bold;"
      " font-size: 16px; margin-top: 15px;'>قل لن يصيبنا إلا ما كتب الله لنا</p>",
      unsafe_allow_html=True,
  )

if show_button:
  if seat_no:
    seat_col = 'رقم الجلوس'

    if seat_col in df.columns:
      clean_input = str(seat_no).strip()
      df[seat_col] = (
          df[seat_col].astype(str).str.strip().str.replace('.0', '', regex=False)
      )

      result = df[df[seat_col] == clean_input]

      if not result.empty:
        st.success('تم العثور على النتيجة بنجاح!')

        student_data = {}
        for col in df.columns:
          vals = result[col].dropna().astype(str).tolist()
          unique_vals = []
          for v in vals:
            v_clean = v.strip()
            if v_clean and v_clean not in unique_vals and v_clean != 'nan':
              unique_vals.append(v_clean)
          student_data[col] = ' '.join(unique_vals)

        base_keys = ['رقم الجلوس', 'اسم الطالب', 'كود الطالب']
        personal_info = {
            k: student_data.get(k, '')
            for k in base_keys
            if k in student_data or k in df.columns
        }
        subjects_info = {
            k: v
            for k, v in student_data.items()
            if k not in base_keys and k != seat_col
        }

        table_html = f"""
                <div class="watermark">نتيجة الفرقة الإعدادية - الترم الاول 2026</div>
                <div class="table-wrapper">
                    <table class='styled-table'>
                        <thead>
                            <tr>
                                <th>بيانات الطالب</th>
                                <th>النتيجة</th>
                            </tr>
                        </thead>
                        <tbody>
                """

        for k, v in personal_info.items():
          if k:
            table_html += f'<tr><td><b>{k}</b></td><td>{v}</td></tr>'

        table_html += f"""
                            <tr>
                                <th style="background-color: #007BFF; color: white; text-align: right; padding: 12px 15px; white-space: nowrap;">المواد</th>
                                <th style="background-color: #007BFF; color: white; text-align: right; padding: 12px 15px; border-right: 2px solid #000000;">التقديرات / الدرجات</th>
                            </tr>
                """

        for k, v in subjects_info.items():
          if k:
            table_html += f'<tr><td><b>{k}</b></td><td>{v}</td></tr>'

        table_html += f"""
                        </tbody>
                    </table>
                    <div class="designer-credit">Designed by Engineer Mohamed Abdelatif Elsayed</div>
                </div>
                """

        st.markdown(table_html, unsafe_allow_html=True)

        st.markdown(
            """
                    <div style="text-align: center; margin-top: 10px;">
                        <button onclick="parent.window.print();" style="background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                            🖨️ طباعة النتيجة
                        </button>
                    </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.error('رقم الجلوس غير موجود، تأكد من الرقم وادخله مرة أخرى.')
    else:
      st.error("عفواً، عمود 'رقم الجلوس' غير متطابق في ملف الإكسيل.")
  else:
    st.warning('الرجاء إدخال رقم الجلوس أولاً.')
