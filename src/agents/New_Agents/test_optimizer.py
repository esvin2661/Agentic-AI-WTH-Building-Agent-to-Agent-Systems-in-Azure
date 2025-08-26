try:
    # Prefer relative import when run as a package
    from .resource_optimizer import ResourceOptimizer
except Exception:
    # Fallback when running as a script (sys.path adjusted)
    from resource_optimizer import ResourceOptimizer


def run_manual_tests():
    # Create optimizer in dry-run (simulation) mode
    opt = ResourceOptimizer(dry_run=True)
    vm = opt.get_vm()
    print("VM fetched for test:", vm)

    # Test CPU high
    rec = opt.recommend_action("cpu", 85)
    print("CPU rec:", rec)
    res = opt.apply_action(rec)
    print("CPU apply result:", res)

    # Test memory low
    rec = opt.recommend_action("memory", 500_000_000)
    print("Memory rec:", rec)
    res = opt.apply_action(rec)
    print("Memory apply result:", res)

    # Test disk I/O
    rec = opt.recommend_action("disk", 6e7)
    print("Disk rec:", rec)
    res = opt.apply_action(rec)
    print("Disk apply result:", res)


if __name__ == "__main__":
    run_manual_tests()
