            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        elapsed = time.perf_counter() - start
        print("方法 2a：power2n(n-1) + power2n(n-1)")
        if completed.returncode == 0:
            print("答案：", completed.stdout.strip())
            print(f"執行時間：{elapsed:.6f} 秒")
        else:
            print("測試失敗：", completed.stderr.strip())
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - start
        print("方法 2a：power2n(n-1) + power2n(n-1)")
        print(f"超過 {timeout_seconds:.1f} 秒仍未完成，已停止測試。")
        print(f"實際等待：約 {elapsed:.3f} 秒")
        print("結果：n=100 時無法在合理時間內完成。")
    print("-" * 48)


def main():
    n = 100
    print(f"比較四種方法，n = {n}")
    print("=" * 48)
    benchmark("方法 1：2 ** n", power2n_method1, n)
    benchmark("方法 2b：遞迴相乘", power2n_method2b, n)
    benchmark("方法 3：遞迴 + 查表（第一次計算）", power2n_method3, n)
    benchmark("方法 3：遞迴 + 查表（第二次直接查表）", power2n_method3, n)
    test_method2a_safely(n, timeout_seconds=1.0)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--only-method2a":
        print(power2n_method2a(int(sys.argv[2])))
    else:
        main()
