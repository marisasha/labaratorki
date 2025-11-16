from regular import PhoneNumberExtractor


if __name__ == "__main__":

    extractor = PhoneNumberExtractor()
    
    # =-=-Поиск телефонов по URL-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    url = "https://moscow.shop.megafon.ru/connect/chnumber/fullnumber"
    
    print(f"\nПоиск по странице: {url}\n")

    phones = extractor.get_phones_from_url(url)
    if phones:
        for i, phone in enumerate(phones, 1):
            print(f"{i:2d}. {phone}")
    else:
        print("Номера не найдены")

    # =-=-Поиск телефонов по тексту-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    print("\nПоиск по тексту:\n")

    test_text = """
    Контактные номера:
    Основной: +7 (495) 123-45-67
    Мобильный: 8 (916) 123-45-67
    Еще: 495-123-45-67
    """
    

    test_phones = extractor.extract_phone_numbers(test_text)
    for phone in test_phones:
        is_valid = extractor.validate_phone_number(phone)
        status = "VALID" if is_valid else "INVALID"
        print(f"{phone} - {status}")

    # =-=-Поиск телефонов по файлу-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    

    print("\nПоиск по файлу\n")
    

    with open("phone.txt","r") as file:
        file_phones = extractor.extract_phone_numbers(file.read())
        for phone in file_phones:
            print(f"{phone}")
