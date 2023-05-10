# Web Application (Django)
---

This project is brought to you by:

* Suramate Chokchaisuwan (Matthew)
* Dhawalrat Leelapratak (New)
* Tanupat Kontha (Prince)

---

### Package Requirement
Please noted that there are several packages required to run the project which can be found in the requirement.txt. However, not all of them are necessarily required.

But, there is one "important" package that must be installed, otherwise, the project can't be run. 

```sh
pipenv install python-dotenv
```

* Remark: Some modules in the project need API Key and Token as authentication. Users can get these credentials from Google API and ThailandPost Token. (Put the credentials in the file and name ".env.secret", It should work without any error 😊)

---

### Buyers [Completed]

- [X] Buyer signup module (using chula domain)

  - [X] Name, telephone (regex), email (regex)

  * E-mail check (can't use the one that already used)
- [X] Buyer login module
- [X] Buyer profile screen (ID, name, telephone, email)

  - [X] Able to edit Name, telephone (regex), email (regex)
- [X] Category browsing screen

  - [X] Have category name and image
- [X] Product browsing screen

  - [X] Based on a category
  - [X] แสดงข้อมูล
    - [X] รูปสินค้า, ชื่อสินค้า, ราคา,
    - [X] ชื่อร้าน และ สถานที่ของร้าน
- [X] Product details screen

  - [X] แสดงข้อมูล รูปสินค้า, ชื่อสินค้า, ราคา
  - [X] ชื่อร้าน และ สถานที่ของร้าน
  - [X] สามารถกดเพิ่มสินค้าเข้าไปในตะกร้าขายของได้
  - [X] สามารถกดลิ้งค์ไปที่ร้านได้
- [X] Shopping Cart screen

  - [X] Show the selected products, quantity, and price
  - [X] Show the total price
  - [X] Buy button to create a transaction

---

### Sellers [Completed]

- [X] Seller signup module

  - [X] Add ชื่อร้าน
  - [X] ชื่อผู้ติดต่อ
  - [X] เบอร์โทร
  - [X] ที่อยู่ร้าน
  - [X] รูปของร้าน (1 picture)
  - [X] รูป QRCode (1 picture)
- [X] Seller login module
- [X] Seller account module (able to edit)

  - [X] ชื่อร้าน
  - [X] ชื่อผู้ติดต่อ
  - [X] เบอร์โทร
  - [X] ที่อยู่ร้าน
  - [X] รูปของร้าน (1 picture)
  - [X] รูป QRCode (1 picture)
- [X] My Product Listing Screen (Show all my products details)

  - [X] ชื่อสินค้า
  - [X] รูปสินค้า
  - [X] หมวดหมู่
  - [X] ราคา
  - [X] สถานะ (ปกติ/หมด)
- [X] Add/Edit/Delete Product Screen

  - [X] ชื่อสินค้า
  - [X] รูปสินค้า
  - [X] หมวดหมู่
  - [X] รายละเอียดสินค้า
  - [X] ราคา
  - [X] สถานะ (ปกติ/หมด)

---
### Additional Parts + Extra

* (EXTRA) in the Project Specification

  - [X] Aesthetic templates
  - [X] Make use of any 3rd parties (API)
  - [X] Shop open-close time
  - [X] Product Search
  - [ ] Publically accessible to cloud service
    -> (Trial and Error) but failed in deployment
* Additional (Not in the Project Specification)

  * JavaScript -> QuerySelector
  * files uploaded check whether it is jpeg or not-> avoid unsupported file types
  * Info Button -> Hover and show info box
  * Modal & Lightbox
  * Image Carousel (Banner)
  * dotenv (securely store API KEY)
  * allowed to transform textarea (more in height) -> practical
  * prepared db.sqlite (4 vendors, 2 customer, 40 products with completed product details/pic/price)
