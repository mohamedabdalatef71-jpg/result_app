import glob
import pandas as pd
import streamlit as st

st.set_page_config(page_title="نتيجة الفرقة الإعدادية", page_icon="🎓")

st.markdown(
    """
    <style>
    direction: rtl;
    text-align: right;
    }
    .stTable {
        text-align: right !important;
    }
    th {
        text-align: right !important;
    }
    td {
        text-align: right !important;
    }
    .watermark-container {
        position: relative;
        text-align: center;
    }
    .watermark-img {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        opacity: 0.12;
        width: 300px;
        z-index: 0;
        pointer-events: none;
    }
    .content-table {
        position: relative;
        z-index: 1;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("نتيجة الفرقة الإعدادية")

excel_files = glob.glob("*.xlsx")
if not excel_files:
  st.error("حط ملف الإكسيل جوه مجلد Result يا معلم!")
else:
  df = pd.read_excel(excel_files[0], dtype=str)
  df.columns = df.columns.astype(str).str.strip()

  seat_input = st.text_input("أدخل رقم الجلوس:")

  if seat_input:
    seat_col = None
    for col in df.columns:
      if "جلوس" in col or "رقم" in col:
        seat_col = col
        break

    if not seat_col:
      seat_col = df.columns[0]

    res = df[df[seat_col].astype(str).str.contains(seat_input.strip(), na=False)]

    if not res.empty:
      st.success("تم العثور على النتيجة بنجاح! 🎉")
      st.markdown("---")

      idx = res.index[0]
      row1 = df.iloc[idx]
      row2 = df.iloc[idx + 1] if idx + 1 < len(df) else pd.Series()

      name_data = []
      other_data = []
      result_data = []

      for col in df.columns:
        if col.startswith("Unnamed"):
          continue

        v1 = str(row1[col]) if col in row1 and str(row1[col]) != "nan" else ""
        v2 = str(row2[col]) if col in row2 and str(row2[col]) != "nan" else ""
        combined_val = f"{v1} {v2}".strip()

        if combined_val.endswith(".0"):
          combined_val = combined_val[:-2]

        if combined_val:
          item = {"النتيجة": combined_val, "البيان / المادة": col}
          if "اسم" in col or "الطالب" in col:
            name_data.append(item)
          elif "مجموع" in col or "النتيجة" in col or "تقدير" in col:
            result_data.append(item)
          else:
            other_data.append(item)

      final_table = name_data + other_data + result_data

      if final_table:
        result_df = pd.DataFrame(final_table)
        
        st.markdown('<div class="watermark-container">', unsafe_allow_html=True)
        try:
            st.markdown('<img src="app/static/logo.jpg" class="watermark-img">', unsafe_allow_html=True)
        except:
            pass
        
        st.markdown('<div class="content-table">', unsafe_allow_html=True)
        st.table(result_df)
        st.markdown('</div></div>', unsafe_allow_html=True)
    else:
      st.error("رقم الجلوس غير موجود، تأكد منه.")