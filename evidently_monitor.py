"""
Evidently AI Monitoring & Data Drift Detection (Step 12)
Monitors feature distributions and data quality between reference and current datasets.
Generates interactive HTML reports and summary logs.
"""

import os
import sys
import numpy as np
import pandas as pd

# Support both Evidently modular architecture and legacy interfaces
try:
    try:
        from evidently.legacy.report import Report
        from evidently.legacy.metric_preset import DataDriftPreset, DataQualityPreset
        from evidently.legacy.test_suite import TestSuite
        from evidently.legacy.test_preset import DataDriftTestPreset
    except ImportError:
        from evidently.report import Report
        from evidently.metric_preset import DataDriftPreset, DataQualityPreset
        from evidently.test_suite import TestSuite
        from evidently.test_preset import DataDriftTestPreset
    EVIDENTLY_AVAILABLE = True
except ImportError as err:
    EVIDENTLY_AVAILABLE = False
    IMPORT_ERR = str(err)


def generate_synthetic_datasets():
    """
    Generate synthetic MLOps production datasets:
    - Reference: Baseline training/validation data
    - Current: Live incoming production data (with induced drift in feature_2_pressure)
    """
    np.random.seed(42)
    n_samples = 300

    # Reference dataset (Baseline)
    ref_feature_1 = np.random.normal(loc=10.0, scale=2.0, size=n_samples)
    ref_feature_2 = np.random.normal(loc=50.0, scale=5.0, size=n_samples)
    ref_target = ref_feature_1 * 1.5 + ref_feature_2 * 0.5 + np.random.normal(0, 1, n_samples)

    reference_data = pd.DataFrame({
        "feature_1_sensor": np.round(ref_feature_1, 2),
        "feature_2_pressure": np.round(ref_feature_2, 2),
        "prediction": np.round(ref_target, 2),
    })

    # Current dataset (Live incoming data: simulated distribution shift in feature_2)
    cur_feature_1 = np.random.normal(loc=10.1, scale=2.1, size=n_samples)
    cur_feature_2 = np.random.normal(loc=58.5, scale=6.0, size=n_samples)  # Drift induced (50 -> 58.5)
    cur_target = cur_feature_1 * 1.5 + cur_feature_2 * 0.5 + np.random.normal(0, 1, n_samples)

    current_data = pd.DataFrame({
        "feature_1_sensor": np.round(cur_feature_1, 2),
        "feature_2_pressure": np.round(cur_feature_2, 2),
        "prediction": np.round(cur_target, 2),
    })

    return reference_data, current_data


def run_evidently_monitoring(output_dir: str = "evidently_reports"):
    """
    Execute Evidently AI Data Drift and Quality Monitoring.
    Saves an interactive HTML report and prints summary results.
    """
    os.makedirs(output_dir, exist_ok=True)
    report_html_path = os.path.join(output_dir, "data_drift_report.html")
    test_html_path = os.path.join(output_dir, "drift_test_suite.html")
    summary_txt_path = os.path.join(output_dir, "monitoring_summary.txt")

    print("=" * 65)
    print("      MLOps Evidently AI Monitoring Pipeline (Step 12)       ")
    print("=" * 65)

    reference_df, current_df = generate_synthetic_datasets()
    print(f"[✓] Generated Reference Dataset : {len(reference_df)} rows")
    print(f"[✓] Generated Current Dataset   : {len(current_df)} rows")

    if not EVIDENTLY_AVAILABLE:
        print(f"[!] Evidently library not fully imported ({IMPORT_ERR}). Running fallback analysis...")
        diff = current_df["feature_2_pressure"].mean() - reference_df["feature_2_pressure"].mean()
        drift_detected = abs(diff) > 3.0
        summary = (
            f"Evidently Fallback Monitoring Summary:\n"
            f"Reference Mean (feature_2_pressure): {reference_df['feature_2_pressure'].mean():.2f}\n"
            f"Current Mean (feature_2_pressure): {current_df['feature_2_pressure'].mean():.2f}\n"
            f"Shift: {diff:+.2f}\n"
            f"Drift Detected: {drift_detected}\n"
        )
        with open(summary_txt_path, "w") as f:
            f.write(summary)
        print(summary)
        return

    # 1. Run Data Drift & Quality Report
    print("\n[+] Calculating Evidently Data Drift & Quality Metrics...")
    report = Report(metrics=[DataDriftPreset(), DataQualityPreset()])
    report.run(reference_data=reference_df, current_data=current_df)
    report.save_html(report_html_path)
    print(f"[✓] Interactive HTML Report saved: {report_html_path}")

    # 2. Run Test Suite for CI/CD assertions
    print("[+] Running Evidently Automated Test Suite...")
    test_suite = TestSuite(tests=[DataDriftTestPreset()])
    test_suite.run(reference_data=reference_df, current_data=current_df)
    test_suite.save_html(test_html_path)
    print(f"[✓] Test Suite HTML Report saved: {test_html_path}")

    # Extract test summary
    test_results = test_suite.as_dict()
    summary_info = test_results.get("summary", {})
    all_passed = summary_info.get("all_passed", False)
    total_tests = summary_info.get("total_tests", 0)
    failed_tests = summary_info.get("failed_tests", 0)

    summary_text = f"""
=================================================================
                 EVIDENTLY AI MONITORING SUMMARY                 
=================================================================
Total Tests Executed : {total_tests}
Passed Tests         : {total_tests - failed_tests}
Failed Tests (Drift) : {failed_tests}
Overall Status       : {'PASSED (No Drift)' if all_passed else 'DRIFT DETECTED (Alert Triggered)'}

Feature Statistics:
- Reference feature_2_pressure mean: {reference_df['feature_2_pressure'].mean():.2f}
- Current feature_2_pressure mean  : {current_df['feature_2_pressure'].mean():.2f} (Shift detected)
- Reference feature_1_sensor mean  : {reference_df['feature_1_sensor'].mean():.2f}
- Current feature_1_sensor mean    : {current_df['feature_1_sensor'].mean():.2f} (Stable)

Output Files Generated:
- Data Drift Interactive Report : {report_html_path}
- Test Suite Interactive Report : {test_html_path}
=================================================================
"""
    with open(summary_txt_path, "w") as f:
        f.write(summary_text)

    print(summary_text)


if __name__ == "__main__":
    run_evidently_monitoring()
