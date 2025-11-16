from regular import PhoneNumberExtractor


if __name__ == "__main__":

    extractor = PhoneNumberExtractor()

    url = "https://moscow.shop.megafon.ru/connect/chnumber/fullnumber"
    
    phones = extractor.get_phones_from_url(url)
    
    print(phones)
