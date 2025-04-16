<h1 align="center">Shortest Path With Genetika Algorithm Kampus UNIB</h1>
<align="center"> Proyek ini akan menampilkan rute terpendek antar lokasi di lingkungan Kampus Universitas Bengkulu menggunakan algoritma Genetika

<h2>Analisis kinerja kode dan algoritma</h2>
Algoritma genetika memiliki sejumlah keunggulan penting dalam menangani masalah optimasi yang rumit. Kemampuannya untuk secara efisien menjelajahi ruang solusi yang luas, menghindari jebakan optimum lokal melalui mekanisme mutasi, serta fleksibilitasnya dalam berbagai jenis permasalahan menjadikannya pilihan yang menarik. Selain itu, sifat adaptif dan kemudahan dalam melakukan paralelisasi memberikan keuntungan dalam hal komputasi. Namun, algoritma ini juga memiliki beberapa kelemahan yang perlu diperhatikan. Proses konvergensi yang kadang-kadang lambat, kesulitan dalam menentukan parameter yang paling sesuai, tantangan dalam merancang representasi solusi yang efektif, serta tidak adanya jaminan untuk menemukan solusi global yang optimal merupakan batasan yang harus diperhatikan dalam penerapannya. Hal ini juga dirasakan oleh kelompok kami, di mana terdapat beberapa aspek yang sulit dilaksanakan akibat kompleksitas algoritma ini.
berikut hasil pengamatan kami:

1. Rute yang diberikan belum sesuai dengan google maps, jalan yang seharusnya satu arah yang dimana mengharuskan user untuk putar arah dan mencari jalan tercepat tidak ditampilkan.
2. Loading untuk menjalankan kode yang telah dibuat masih tergolong lambat
3. tidak bisa melihat salah satu jalur( motor saja, atau jalan kaki saja , atau mobilsaja)

pertama, masalah yang kami temukan no 1 dan 3 yaitu jalan antar gedung yang tidak dapat di akses dengan satu arah sesuai dengan peraturan Jalan Universitas Bengkulu akan menyebabkan beberapa komplikasi pada sistem kami yaitu sistem makin lambat, serta rentan akan eror, hal ini juga berlaku untuk  tidak bisa melihat salah satu jalur . kedua, yang paling berdampak dari algoritma ini adalah bagian loading saat memuat inputan yang di inginkan, dalam proses ini user tidak dapat memasukan tempat yang tidak sesuai dengan yang ada pada inputan peta. misalkan, dekanat dan Dekanat. input dekanat (dengan huruf d kecil), tidak akan ter baca oleh sistem karena yang ada pada maps adalah Dekanat (menggunakan D Kapital). karena menginputtkan darta dari banyaknya fungsi ini akan menjadi salah satu dari banyak faktor mengapa proses memuat data apada program kami lambat.
