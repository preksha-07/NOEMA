def display_metrics(classical, optimized):
    print("\n========== 📊 METRICS PANEL ==========")

    print("\n🔴 CLASSICAL PATH")
    print(f"Distance: {round(classical['distance'], 2)}")
    print(f"Time:     {round(classical['time'], 2)}")
    print(f"Risk:     {round(classical['risk'], 2)}")
    print(f"Cost:     {round(classical['cost'], 2)}")

    print("\n🟢 OPTIMIZED PATH")
    print(f"Distance: {round(optimized['distance'], 2)}")
    print(f"Time:     {round(optimized['time'], 2)}")
    print(f"Risk:     {round(optimized['risk'], 2)}")
    print(f"Cost:     {round(optimized['cost'], 2)}")

    print("\n📈 IMPROVEMENT")
    improvement = ((classical['cost'] - optimized['cost']) / classical['cost']) * 100
    print(f"Cost Reduction: {round(improvement, 2)}%")