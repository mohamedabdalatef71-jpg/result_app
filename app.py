import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


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
        st.markdown(
            '<div style="text-align: center; color: green; font-weight:'
            ' bold; margin-bottom: 10px;">تم العثور على النتيجة بنجاح!</div>',
            unsafe_allow_html=True,
        )

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

        table_rows_html = ''
        for k, v in personal_info.items():
          if k:
            table_rows_html += f'<tr><td><b>{k}</b></td><td>{v}</td></tr>'

        table_rows_html += """
            <tr>
                <th colspan="2" style="background-color: #007BFF; color: white; text-align: center; padding: 12px 15px; font-size: 18px;">المواد والتقديرات</th>
            </tr>
        """

        for k, v in subjects_info.items():
          if k:
            table_rows_html += f'<tr><td><b>{k}</b></td><td>{v}</td></tr>'

        final_html = f"""
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: sans-serif;
                    background-color: transparent;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .result-container {{
                    border: 3px solid #007BFF;
                    border-radius: 15px;
                    padding: 25px;
                    background-color: #ffffff;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                    position: relative;
                    width: 100%;
                    max-width: 650px;
                    margin: 0 auto;
                }}
                .header-box {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #007BFF;
                    padding-bottom: 10px;
                }}
                .table-wrapper {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%;
                }}
                .styled-table {{
                    direction: rtl;
                    border-collapse: collapse;
                    font-size: 16px;
                    background-color: #ffffff;
                    color: #000000;
                    border: 2px solid #000000;
                    border-radius: 10px;
                    overflow: hidden;
                    width: 100%;
                }}
                .styled-table th {{
                    background-color: #007BFF;
                    color: white;
                    padding: 12px 15px;
                    font-size: 18px;
                    border: 2px solid #000000;
                    text-align: right;
                }}
                .styled-table td {{
                    padding: 10px 15px;
                    border: 2px solid #000000;
                    color: #000000;
                    font-weight: bold;
                }}
                .styled-table td:nth-child(1) {{ 
                    text-align: right; 
                    width: 45%;
                }}
                .styled-table td:nth-child(2) {{ 
                    text-align: right; 
                    width: 55%;
                }}
                .styled-table tbody tr:nth-of-type(even) {{ background-color: #f9f9f9; }}
                .styled-table tbody tr:nth-of-type(odd) {{ background-color: #ffffff; }}
                .designer-credit {{
                    text-align: center;
                    font-size: 14px;
                    font-weight: bold;
                    color: #555555;
                    margin-top: 20px;
                }}
                .watermark {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%) rotate(-30deg);
                    font-size: 50px;
                    font-weight: bold;
                    color: rgba(0, 123, 255, 0.05);
                    z-index: 0;
                    pointer-events: none;
                    white-space: nowrap;
                }}
            </style>
        </head>
        <body>
            <div class="result-container">
                <div class="watermark">Mohamed Abdalatef</div>
                <div class="header-box">
                    <div style="font-size: 16px; font-weight: bold; color: #007BFF;">Mohamed Abdalatef</div>
                    <div style="font-size: 18px; font-weight: bold; color: #007BFF;">نتيجة الفرقة الإعدادية - الترم الأول 2026</div>
                    <div style="width: 80px;"></div>
                </div>
                
                <div class="table-wrapper">
                    <table class='styled-table'>
                        <thead>
                            <tr>
                                <th>بيانات الطالب</th>
                                <th>النتيجة</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows_html}
                        </tbody>
                    </table>
                </div>
                <div class="designer-credit">Designed by Engineer Mohamed Abdelatif Elsayed</div>
            </div>
        </body>
        </html>
        """

        components.html(final_html, height=600, scrolling=True)

        print_button_html = """
        <div style="text-align: center; margin-top: 15px;">
            <button onclick="parent.window.print();" style="background-color: #28a745; color: white; padding: 12px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 300px;">
                🖨️ طباعة النتيجة
            </button>
        </div>
        """
        components.html(print_button_html, height=75)

      else:
        st.error('رقم الجلوس غير موجود، تأكد من الرقم وادخله مرة أخرى.')
    else:
      st.error("عفواً، عمود 'رقم الجلوس' غير متطابق في ملف الإكسيل.")
  else:
    st.warning('الرجاء إدخال رقم الجلوس أولاً.')
