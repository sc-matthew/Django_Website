# Web Application (Django)

---

This project is brought to you by:

* Suramate Chokchaisuwan (Matthew)
* Dhawalrat Leelapratak (New)
* Tanupat Kontha (Prince)

---

### Buyers

- [X] Buyer signup module (using chula domain)
  - [X] Name, telephone (regex), email (regex)
- [X] Buyer login module
- [ ] Buyer profile screen (ID, name, telephone, email)
  - [X] Able to edit Name, telephone (regex), email (regex)
- [ ] Category browsing screen
  - [ ] Have category name and image
- [X] Product browsing screen
  - [X] Based on a category
  - [X] แสดงข้อมูล
    - [X] รูปสินค้า, ชื่อสินค้า, ราคา,
    - [ ] ชื่อร้าน และ สถานที่ของร้าน
- [X] Product details screen
  - [x] แสดงข้อมูล รูปสินค้า, ชื่อสินค้า, ราคา
  - [ ] ชื่อร้าน และ สถานที่ของร้าน
  - [ ] สามารถกดเพิ่มสินค้าเข้าไปในตะกร้าขายของได้
  - [ ] สามารถกดลิ้งค์ไปที่ร้านได้
- [X] Shopping Cart screen
  - [X] Show the selected products, quantity, and price
  - [X] Show the total price
  - [X] Buy button to create a transaction

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

* Additional Parts (Extra marks)
  * 1
    * Proudly presented : JavaScript -> QuerySelector
    * drop-down list to separate postData + postFiles
    * files uploaded check whether it is jpeg or not -> avoid unsupported file types
    * Info Button -> Hover and show info box
    * Modal & Lightbox
    * Currency omitted -> Automatically filled in (TM TG)
  * 2
    * Image Carousel (Banner)

---

Memo updated list:

* Already merged from prince_new branch to main branch

---

Matthew:

- [ ] module edit product details (link to ดินสอ)
- [ ] edit nav bar

New:

- [ ] add /edit ให้ show ว่าซ้ำไหม (unique)
  1. edit success -> no show after save (pop-up & return)
  2. duplicate value -> error page  (red warning)

Prince:

- [ ] delete product (link to trash)
  1. pop-up (confirmation to delete)
  2. delete successful
  3. press ok (redirect to manage product page)

---

Remain after finish buyer:

- [ ] link details href to buyers product details info
