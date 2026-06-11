from manager.real_estate_manager import RealEstateManager

def main():
    mgr = RealEstateManager("real_estate_demo.db")
    # показать всё
    print("--- Квартиры ---")
    for a in mgr.get_all_apartments():
        print(a.get_info())
    print("\n--- Клиенты ---")
    for c in mgr.get_all_clients():
        print(c.get_info())
    print("\n--- Сделки ---")
    for d in mgr.get_all_deals():
        print(d.get_info(mgr))

    # бизнес-методы
    apt = mgr.get_apartment(2)
    if apt:
        print(f"\nЦена за м²: {apt.price_per_sqm():.2f}")
    if apt:
        print(f"На высоком этаже? {apt.is_on_high_floor()}")

    deal = mgr.get_deal(2)
    if deal:
        print(f"Активация сделки 2: {deal.activate()}")
        mgr.update_deal(deal)
        print(f"Завершение: {deal.complete()}")
        mgr.update_deal(deal)
        print(f"Новый статус: {deal.deal_status.value}")

    # поиск
    found = mgr.find_apartments_by_city("Максаковка")
    print(f"\nКвартиры в Москве: {len(found)}")
    for a in found:
        print(a.get_info())

if __name__ == "__main__":
    main()