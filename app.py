import streamlit as st
import PyPDF2
from pdf2image import convert_from_bytes
import io
import zipfile
import os
from PIL import Image
import math

st.set_page_config(page_title="PDFツール", page_icon="📄", layout="wide")
st.title("📄 PDFツール")
st.caption("ページ並び替え・結合・画像変換ができます")

tab1, tab2, tab3 = st.tabs(["🔀 並び替え・回転", "📎 PDF結合", "🖼️ 画像変換"])


# ==========================
# 共通：プレビュー表示関数
# ==========================
def show_preview(pdf_bytes, rotations=None, columns=4):
    if rotations is None:
        rotations = {}
    try:
        images = convert_from_bytes(pdf_bytes, dpi=72)
        total = len(images)
        st.subheader(f"📋 プレビュー（全{total}ページ）")
        rows = math.ceil(total / columns)
        for row in range(rows):
            cols = st.columns(columns)
            for col_idx in range(columns):
                page_idx = row * columns + col_idx
                if page_idx >= total:
                    break
                img = images[page_idx]
                angle = rotations.get(page_idx, 0)
                if angle:
                    img = img.rotate(-angle, expand=True)
                with cols[col_idx]:
                    st.image(img, caption=f"p.{page_idx + 1}", use_column_width=True)return images
    except Exception as e:
        st.error(f"プレビューの表示に失敗しました：{e}")
        
        return []


# ==========================
# 機能1：並び替え・回転
# ==========================
with tab1:
    st.header("ページの並び替え・回転")
    uploaded = st.file_uploader("PDFをアップロード", type="pdf", key="reorder")

    if uploaded:
        pdf_bytes = uploaded.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        total = len(reader.pages)
        st.info(f"総ページ数：{total} ページ（ページ番号は1から始まります）")

        # ---① 並び順---
        st.subheader("① ページの並び順")
        default_order = ",".join(str(i) for i in range(1, total + 1))
        order_input = st.text_input(
            "ページ番号をカンマ区切りで入力してください",
            value=default_order,
            help="例）2,1,3 → 1ページ目と2ページ目を入れ替え"
        )

        # --- ② 回転（ボタン式） ---
        st.subheader("② 回転させるページ")

        if "rotations" not in st.session_state:
            st.session_state.rotations = {}

        rotate_pages = st.multiselect(
            "回転させるページを選んでください（複数選択可）",
            options=list(range(1, total + 1)),
            format_func=lambda x: f"p.{x}"
        )

        if rotate_pages:
            st.write("各ページの回転方向を選んでください：")
            cols_header = st.columns([1, 2, 2, 2, 1])
            cols_header[0].markdown("**ページ**")
            cols_header[1].markdown("**↺ 左に90°**")
            cols_header[2].markdown("**↕ 逆さに**")
            cols_header[3].markdown("**↻ 右に90°**")
            cols_header[4].markdown("**🔄 リセット**")

            for pg in rotate_pages:
                idx = pg - 1
                current = st.session_state.rotations.get(idx, None)
                cols = st.columns([1, 2, 2, 2, 1])
                cols[0].markdown(f"**p.{pg}**")

                if cols[1].button("↺ 左90°", key=f"left_{pg}",
                                  type="primary" if current == 270 else "secondary"):
                    st.session_state.rotations[idx] = 270
                    st.rerun()

                if cols[2].button("↕ 逆さ", key=f"flip_{pg}",
                                  type="primary" if current == 180 else "secondary"):
                    st.session_state.rotations[idx] = 180
                    st.rerun()

                if cols[3].button("↻ 右90°", key=f"right_{pg}",
                                  type="primary" if current == 90 else "secondary"):
                    st.session_state.rotations[idx] = 90
                    st.rerun()

                if cols[4].button("🔄", key=f"reset_{pg}"):
                    st.session_state.rotations.pop(idx, None)
                    st.rerun()

            if st.session_state.rotations:
                label_map = {90: "右90°", 180: "逆さ", 270: "左90°"}
                settings = [
                    f"p.{i+1}→{label_map[v]}"
                    for i, v in st.session_state.rotations.items()
                ]
                st.caption(f"現在の回転設定：{' / '.join(settings)}")

        # --- プレビュー ---
        st.divider()
        with st.expander("🔍 プレビューを表示する", expanded=True):
            show_preview(pdf_bytes, rotations=st.session_state.rotations)

        # --- 実行ボタン ---
        st.divider()
        if st.button("✅ 実行してダウンロード", key="btn_reorder"):
            try:
                page_order = [int(p.strip()) - 1 for p in order_input.split(",")]
                rotations = st.session_state.rotations

                writer = PyPDF2.PdfWriter()
                reader2 = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

                for original_idx in page_order:
                    page = reader2.pages[original_idx]
                    if original_idx in rotations:
                        page.rotate(rotations[original_idx])
                    writer.add_page(page)

                output = io.BytesIO()
                writer.write(output)
                output.seek(0)

                st.success("✅ 完了しました！")
                st.download_button(
                    label="📥 PDFをダウンロード",
                    data=output,
                    file_name="reordered_output.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"エラーが発生しました：{e}")


# ==========================
# 機能2：PDF結合
# ==========================
with tab2:
    st.header("複数PDFの結合")
    uploaded_files = st.file_uploader(
        "PDFをアップロード（複数可）",
        type="pdf",
        accept_multiple_files=True,
        key="merge"
    )

    if uploaded_files:
        st.subheader("結合順の確認・変更")
        for i, f in enumerate(uploaded_files, 1):
            st.write(f"{i}. {f.name}")

        order_input = st.text_input(
            "順番を変更する場合は番号をカンマ区切りで入力（そのままでよければ空欄）",
            placeholder="例）2,1,3"
        )

        with st.expander("🔍 各PDFのプレビューを表示する"):
            for i, f in enumerate(uploaded_files, 1):
                st.markdown(f"**{i}. {f.name}**")
                f.seek(0)
                show_preview(f.read(), columns=4)
                st.divider()

        if st.button("✅ 結合してダウンロード", key="btn_merge"):
            try:
                if order_input.strip():
                    order = [int(p.strip()) - 1 for p in order_input.split(",")]
                    sorted_files = [uploaded_files[i] for i in order]
                else:
                    sorted_files = uploaded_files

                writer = PyPDF2.PdfWriter()
                for f in sorted_files:
                    f.seek(0)
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        writer.add_page(page)

                output = io.BytesIO()
                writer.write(output)
                output.seek(0)

                st.success("✅ 完了しました！")
                st.download_button(
                    label="📥 PDFをダウンロード",
                    data=output,
                    file_name="merged_output.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"エラーが発生しました：{e}")


# ==========================
# 機能3：PDF → 画像変換
# ==========================
with tab3:
    st.header("PDF → 画像変換")
    uploaded = st.file_uploader("PDFをアップロード", type="pdf", key="convert")

    if uploaded:
        pdf_bytes = uploaded.read()
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        total = len(reader.pages)
        st.info(f"総ページ数：{total} ページ")

        col1, col2 = st.columns(2)
        with col1:
            page_input = st.text_input(
                "変換するページ",
                value="all",
                help="all で全ページ / 1,3,5 で個別指定 / 1-5 で範囲指定"
            )
        with col2:
            dpi = st.selectbox(
                "画質（DPI）",
                options=[72, 150, 300],
                index=1,
                format_func=lambda x: {
                    72: "低画質(72dpi)",
                    150: "標準(150dpi)◀推奨",
                    300: "高画質(300dpi)"
                }[x]
            )

        fmt = st.radio("画像形式", ["PNG", "JPEG"], horizontal=True)

        with st.expander("🔍 プレビューを表示する", expanded=True):
            show_preview(pdf_bytes, columns=4)

        if st.button("✅ 変換してダウンロード", key="btn_convert"):
            try:
                if page_input.strip().lower() == "all":
                    page_numbers = list(range(1, total + 1))
                elif "-" in page_input:
                    start, end = page_input.split("-")
                    page_numbers = list(range(int(start), int(end) + 1))
                else:
                    page_numbers = [int(p.strip()) for p in page_input.split(",")]

                with st.spinner("変換中...しばらくお待ちください"):
                    images = convert_from_bytes(
                        pdf_bytes,
                        dpi=dpi,
                        first_page=min(page_numbers),
                        last_page=max(page_numbers)
                    )

                base_name = os.path.splitext(uploaded.name)[0]
                ext = ".png" if fmt == "PNG" else ".jpg"
                zip_buffer = io.BytesIO()

                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    start_page = min(page_numbers)
                    for i, image in enumerate(images):
                        current_page = start_page + i
                        if current_page in page_numbers:
                            img_buffer = io.BytesIO()
                            image.save(img_buffer, fmt)
                            img_buffer.seek(0)
                            zf.writestr(
                                f"{base_name}_p{current_page:03d}{ext}",
                                img_buffer.read()
                            )

                zip_buffer.seek(0)
                st.success(f"✅ {len(images)}枚の画像に変換しました！")
                st.download_button(
                    label="📥 ZIPでダウンロード",
                    data=zip_buffer,
                    file_name=f"{base_name}_images.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"エラーが発生しました：{e}")
