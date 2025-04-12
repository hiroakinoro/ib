# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 18:38:11 2025

@author: h-noro
"""

import streamlit as st
import pandas as pd

# タイトル
st.title("ib データ選択アプリ")

# CSVアップロード
uploaded_file = st.file_uploader("オリジナルデータ（CSV）をアップロードしてください", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding="shift-jis")

    # 「-」の名前は除外
    df = df[df["1. Name"] != "-"]

    selected_rows = []

    for name, group in df.groupby("1. Name"):
        st.subheader(f"さん: {name}")
        test_dates = group["14. Test Date / Time"].unique()
        selected_date = st.selectbox(f"{name} さんの測定日を選んでください", test_dates, key=name)
        selected_row = group[group["14. Test Date / Time"] == selected_date]
        if not selected_row.empty:
            selected_rows.append(selected_row.iloc[0])

    if selected_rows:
        result_df = pd.DataFrame(selected_rows).reset_index(drop=True)
        st.write("✅ 選択されたデータ", result_df)

        # CSVとして書き出し
        csv_bytes = result_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

        st.download_button(
            label="💾 CSVをダウンロード",
            data=csv_bytes,
            file_name="ib_output.csv",
            mime="text/csv"
        )
