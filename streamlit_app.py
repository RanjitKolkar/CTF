import streamlit as st
import json
import pandas as pd
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Digital Forensics CTF",
    page_icon="🕵️",
    layout="wide"
)

DATA_FILE = "submissions.json"
LOADER_FILE = "load_ctf.sh"

# ---------------- Helpers ----------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ---------------- Sidebar ----------------
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Submit Flags", "Leaderboard"]
)

# =======================
# DASHBOARD
# =======================
if page == "Dashboard":
    st.title("🧬 Digital Forensics CTF – Instructions")

    st.subheader("📥 Step 1: Download CTF Loader")
    st.download_button(
        label="⬇️ Download load_ctf.sh",
        data=open(LOADER_FILE, "rb").read(),
        file_name="load_ctf.sh"
    )

    st.subheader("🖥️ Step 2: Run on Ubuntu")
    st.code(
        """
chmod +x load_ctf.sh
./load_ctf.sh
        """,
        language="bash"
    )

    st.subheader("🧪 Step 3: Solve the Challenges")
    st.markdown(
        """
- 5 Digital Forensics challenges will be created
- Flags are **not directly visible**
- Use Ubuntu forensic tools only
- Flag format: `FLAG{...}`
        """
    )

    st.subheader("📤 Step 4: Prepare solution.txt")
    st.markdown(
        """
Create a file named **solution.txt** containing:
- Commands executed
- Steps followed for each challenge

❌ Do NOT write flags inside solution.txt  
✅ Only methodology / commands
        """
    )

    st.subheader("📤 Step 5: Submit")
    st.markdown(
        """
- Go to **Submit Flags**
- Enter Roll Number
- Enter all 5 flags
- Upload `solution.txt`
- Submission time will be recorded automatically
        """
    )

    st.warning("⚠️ Sharing flags or solution files is treated as malpractice.")

    st.subheader("💡 Hints")
    st.markdown(
        """
    The following hints can be used to get the flags accross 5 challenges
    """
    )

    with st.expander("Hints"):
        st.code(
            """
    ls 
    file
    chmod
    cat
    strings
    xxd
    grep
    stat
    getfattr
    cat
    rev
    base64
            """,
            language="bash"
        )

# =======================
# SUBMIT FLAGS
# =======================
elif page == "Submit Flags":
    st.title("📤 Flag & Solution Submission")

    roll = st.text_input("Roll Number")

    flags = {}
    for i in range(1, 6):
        flags[f"Challenge{i}"] = st.text_input(
            f"Flag for Challenge {i}"
        )

    solution_file = st.file_uploader(
        "Upload solution.txt (commands / steps only)",
        type=["txt"]
    )

    if st.button("🚀 Submit"):
        if not roll or any(v.strip() == "" for v in flags.values()):
            st.error("Please enter Roll Number and all 5 flags.")
        elif solution_file is None:
            st.error("Please upload solution.txt file.")
        else:
            data = load_data()

            # prevent duplicate submission
            if any(d["roll"] == roll for d in data):
                st.warning("⚠️ You have already submitted.")
            else:
                submission = {
                    "roll": roll,
                    "flags": flags,
                    "solution_text": solution_file.read().decode("utf-8"),
                    "timestamp": datetime.now().isoformat()
                }

                data.append(submission)
                save_data(data)

                st.success("✅ Submission successful!")
                st.write("🕒 Submission Time:", submission["timestamp"])

# =======================
# LEADERBOARD
# =======================
elif page == "Leaderboard":
    st.title("🏆 Leaderboard (Fastest Submissions)")

    data = load_data()

    if not data:
        st.info("No submissions yet.")
    else:
        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        st.dataframe(
            df[["roll", "timestamp"]].reset_index(drop=True),
            use_container_width=True
        )

        st.caption(
            "Ranking is based on submission time only. "
            "Flag correctness and solution methodology are verified by faculty."
        )
