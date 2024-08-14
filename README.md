# Auto_Cardscanner_Project

![MasterHead](https://resmim.net/cdn/2024/08/14/WJHbRL.png)
![MasterHead](https://resmim.net/cdn/2024/08/14/WJHrTW.png)
![MasterHead](https://resmim.net/cdn/2024/08/14/WJHsO3.png)

English(İngilizce)

This Python code sequentially processes JPEG images from a specified directory by uploading them to the [cardscanner.co](https://www.cardscanner.co/) website and extracting the text from these images, which is then saved to a text file. The code starts by initializing a web browser with specific options to ensure stability and performance. Once the browser is set up, the code scans the directory for JPEG images and begins processing them.

The main function of the code is to handle each image one by one, first verifying that the file exists and hasn’t been processed before. If the file is found and hasn't been processed, the code uploads the image to the website and attempts to extract the text. This process includes a retry mechanism, allowing the code to try the operation multiple times if any errors occur. If the extraction is successful, the extracted text is appended to a file. If any issues arise during the process, they are logged, and the process is retried. After all images have been processed, the browser is closed, and the operation is completed.



Turkish(Türkçe)

Bu Python kodu, belirli bir klasörde bulunan JPEG formatındaki görselleri sırayla alarak [cardscanner.co](https://www.cardscanner.co/) internet sitesine yükler ve görsellerdeki metinleri çıkararak bir metin dosyasına kaydeder. Kod, her bir görseli işlemden geçirmeden önce, tarayıcıyı başlatır ve belirtilen internet sitesine erişir. Ardından, belirlenen klasördeki görselleri tarayarak uygun formatta olanları seçer ve bu görselleri işlemeye başlar.

Kodun ilk aşamasında, tarayıcıyı başlatmak için gerekli seçenekler belirlenir. Bu seçenekler, tarayıcının daha kararlı ve hızlı çalışmasını sağlamak amacıyla optimize edilmiştir. Tarayıcı başlatıldıktan sonra, klasördeki tüm JPEG görselleri bir döngü ile taranır. Her bir görsel için, öncelikle dosyanın var olup olmadığı kontrol edilir. Eğer dosya bulunamazsa ya da daha önce işlenmişse, bu görsel atlanır ve bir sonraki görsele geçilir.

Her görsel için metin çıkarma işlemi, belirli bir hata denetim mekanizmasıyla gerçekleştirilir. Bu mekanizma, eğer bir hata ile karşılaşılırsa işlemi belirli bir sayıda yeniden denemeye olanak tanır. Görsel başarıyla yüklendiğinde ve metin çıkarma işlemi tamamlandığında, elde edilen metin bir dosyaya eklenir. İşlem sırasında herhangi bir hata oluşursa, bu hata günlükte belirtilir ve işlem yeniden denenir. Tüm görseller işlendiğinde, tarayıcı kapatılır ve işlem sonlandırılır.

![MasterHead](https://images.pexels.com/photos/27773407/pexels-photo-27773407.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1)
