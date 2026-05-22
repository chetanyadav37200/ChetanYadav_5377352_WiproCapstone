import os
import subprocess
import shutil
import sys

if __name__ == "__main__":
    print("\n====================================================================")
    print("🚀 INITIALIZING BDD ENTERPRISE TESTING AUTOMATION MATRIX FUNNEL")
    print("====================================================================\n")

    # Define paths for our tracking directories
    results_dir = "reports/allure-results"
    report_output_dir = "reports/allure-report"
    history_dir = os.path.join(report_output_dir, "history")
    results_history_dir = os.path.join(results_dir, "history")

    # Ensure our structural reporting folders exist natively
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)

    # --------------------------------------------------------------------
    # CRITICAL CORES: Copy past historical data blocks so Allure appends them
    # --------------------------------------------------------------------
    if os.path.exists(history_dir):
        if os.path.exists(results_history_dir):
            shutil.rmtree(results_history_dir)
        shutil.copytree(history_dir, results_history_dir)
        print("📊 Natively injected historical analytics nodes into current results matrix.")

    # ====================================================================
    # 🎯 TEST SELECTION SECTOR
    # ====================================================================
    # Change your tags here between runs as you normally do!
    target_tag = " --tags=@test2"
    # ====================================================================

    cmd = f"behave -f allure_behave.formatter:AllureFormatter -o {results_dir} features{target_tag}"

    print(f"📋 Executing Test Command Suite Suite: {cmd}")
    print("--------------------------------------------------------------------")

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Test suite execution terminated with exit faults: {e.returncode}")
    except KeyboardInterrupt:
        print("\n🛑 Execution sweep forcefully interrupted by developer.")
        sys.exit(1)

    print("\n--------------------------------------------------------------------")
    print("📊 COMPILING STATIC ARCHIVE MATRIX AND LAUNCHING STABLE ALLURE PORTAL")
    print("====================================================================\n")

    # 1. Physically compile the independent JSON blocks into a concrete history summary report
    compile_cmd = f"allure generate {results_dir} -o {report_output_dir} --clean"
    print(f"🔨 Compiling data files: {compile_cmd}")
    subprocess.run(compile_cmd, shell=True)

    # 2. Host the cumulative folder tree rather than volatile real-time memory caches
    try:
        os.system(f"allure open {report_output_dir}")
    except KeyboardInterrupt:
        print("\n👋 Allure reporting framework hosting terminated safely.")