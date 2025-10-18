import os
import sys
import datetime as _dt
from typing import List, Dict

try:
    import pyautogui  # type: ignore
except Exception as e:
    print("pyautogui import failed. Will try fallback after install. Error:", e)
    pyautogui = None  # type: ignore

try:
    from PIL import ImageDraw, ImageFont  # type: ignore
except Exception:
    # Pillow is usually installed with pyautogui, but just in case
    print("Pillow is required. Install with: pip install pillow")
    raise

# Optional fallback: mss for screenshotting if pyautogui fails
try:
    import mss  # type: ignore
    import mss.tools  # type: ignore
except Exception:
    mss = None  # type: ignore


# ========== Configuration ==========
# Change this to your name if different
USER_NAME = os.environ.get("SCREENSHOT_USER", "varun k n")

# Root of workspace (folder containing this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tasks and required screenshots (description -> filename prefix)
WORK_ITEMS: List[Dict] = [
    {
        "task": "task1-java-backend",
        "title": "Task 1: Java Backend",
        "shots": [
            ("maven_package_success", "Terminal showing: mvn package success"),
            ("api_get_tasks", "GET /api/tasks response (browser/Postman/curl)"),
            ("api_create_task", "POST /api/tasks create request+response"),
            ("api_update_task", "PUT /api/tasks/{id} update request+response"),
            ("api_delete_task", "DELETE /api/tasks/{id} response"),
            ("api_search", "GET /api/tasks/search?name=... response"),
        ],
    },
    {
        "task": "task2-kubernetes",
        "title": "Task 2: Kubernetes",
        "shots": [
            ("kubectl_get_pods", "kubectl get pods -n default (or your namespace)"),
            ("kubectl_get_svc", "kubectl get svc and NodePort/ClusterIP details"),
            ("kubectl_logs", "kubectl logs <task-manager-pod> showing app logs"),
            ("kubectl_pv_pvc", "kubectl get pv,pvc and/or describe"),
            ("app_access", "Browser hitting service (NodePort/minikube service)"),
        ],
    },
    {
        "task": "task3-react-frontend",
        "title": "Task 3: React Frontend",
        "shots": [
            ("home_page", "Frontend home page loaded"),
            ("search_feature", "Search tasks by name UI working"),
            ("create_update_form", "Create/Update form filled and submit result"),
            ("execution_timeline", "Execution history/timestamps visible"),
        ],
    },
    {
        "task": "task4-cicd-pipeline",
        "title": "Task 4: CI/CD Pipeline",
        "shots": [
            ("actions_run", "GitHub Actions run success (jobs view)"),
            ("dockerhub_image", "Docker Hub repo showing built image and tags"),
            ("k8s_deploy_updated", "Kubernetes deployment updated to new image"),
        ],
    },
    {
        "task": "task5-data-science",
        "title": "Task 5: Data Science",
        "shots": [
            ("notebook_cells", "Notebook executed cells (key steps)"),
            ("accuracy_metrics", "Model accuracy/metrics table or chart"),
        ],
    },
]


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _load_font(size: int = 18) -> ImageFont.FreeTypeFont:
    # Try to load a common Windows font; fallback to default
    font_paths = [
        r"C:\\Windows\\Fonts\\arial.ttf",
        r"C:\\Windows\\Fonts\\segoeui.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _capture_raw_image():
    """Capture a PIL Image using pyautogui or mss fallback."""
    # Try pyautogui first
    if pyautogui is not None:
        try:
            return pyautogui.screenshot()
        except Exception as e:
            print(f"pyautogui.screenshot failed: {e}")
    # Fallback to mss
    if mss is not None:
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # primary monitor
                sct_img = sct.grab(monitor)
                from PIL import Image
                return Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        except Exception as e:
            print(f"mss capture failed: {e}")
    raise RuntimeError("No screenshot backend available. Install pyautogui or mss and ensure a graphical session is active.")


def capture_with_watermark(save_path: str, header: str) -> None:
    img = _capture_raw_image()  # PIL Image
    draw = ImageDraw.Draw(img, "RGBA")

    timestamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"{header} | Name: {USER_NAME} | {timestamp}"

    # Draw semi-transparent bar at bottom
    W, H = img.size
    pad = 10
    font = _load_font(20)
    text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:]
    bar_h = text_h + pad * 2
    draw.rectangle([(0, H - bar_h), (W, H)], fill=(0, 0, 0, 140))
    draw.text((pad, H - bar_h + pad), text, fill=(255, 255, 255, 255), font=font)

    img.save(save_path)


def prompt_and_capture(task_dir: str, title: str, shots: List, root_dir: str) -> None:
    dest_dir = os.path.join(root_dir, task_dir, "screenshots")
    _ensure_dir(dest_dir)
    print(f"\n=== {title} ===")
    print("For each item below: Arrange your screen to show the requested content, then press Enter (just press the key) to capture. Type 's' to skip, 'q' to stop. You can also type 'c' or 'enter' then Enter to capture.")

    for prefix, desc in shots:
        while True:
            ans = input(f"\nReady to capture: {desc}\n[Press Enter to capture | s=Skip | q=Quit | c/enter=Capture]: ").strip().lower()
            if ans == "q":
                return
            if ans == "s":
                print("Skipped.")
                break
            if ans in ("", "c", "enter", "capture", "y"):  # accept common inputs for capture
                ts = _dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"{prefix}_{ts}.png"
                path = os.path.join(dest_dir, filename)
                try:
                    capture_with_watermark(path, header=desc)
                    print(f"Saved: {path}")
                except Exception as e:
                    print(f"Failed to capture: {e}")
                break
            print("Unrecognized input. Press Enter, 's', or 'q'.")


def main() -> int:
    print("Guided screenshot capture will help you collect all required images per task.")
    print("Tip: Open terminals, browsers, Postman, or notebooks in advance for faster capture.")
    print(f"Watermark will include your name as: {USER_NAME}. To change, set SCREENSHOT_USER env var.")

    # Quick sanity check for workspace structure
    expected = [w["task"] for w in WORK_ITEMS]
    missing = [t for t in expected if not os.path.isdir(os.path.join(BASE_DIR, t))]
    if missing:
        print("Warning: The following task folders were not found; their screenshots will still be saved alongside this script:")
        for m in missing:
            print(f" - {m}")

    # Sanity test: try capturing a quick sanity image once
    try:
        sanity_dir = os.path.join(BASE_DIR, "_sanity_screenshots")
        _ensure_dir(sanity_dir)
        sanity_path = os.path.join(sanity_dir, _dt.datetime.now().strftime("sanity_%Y-%m-%d_%H-%M-%S.png"))
        capture_with_watermark(sanity_path, header="Sanity capture")
        print(f"Sanity screenshot OK: {sanity_path}")
    except Exception as e:
        print("Sanity screenshot failed. Please check:")
        print(" - You are running on a desktop session (not headless)")
        print(" - Python packages installed: pyautogui pillow (and optionally mss)")
        print(" - Try running terminal normally (not elevated) and ensure no RDP lock screen")
        print(f"Error: {e}")

    for item in WORK_ITEMS:
        task_dir = item["task"]
        title = item["title"]
        shots = item["shots"]

        # choose save root: task folder if exists, else current dir
        root = BASE_DIR if os.path.isdir(os.path.join(BASE_DIR, task_dir)) else BASE_DIR
        prompt_and_capture(task_dir, title, shots, root)

    print("\nAll done. Images saved under each task's 'screenshots' folder.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
