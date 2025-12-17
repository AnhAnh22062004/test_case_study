# Process Documentation - Image Resize Tool

## 1. Tại sao lại lựa chọn PILLOW trong khi có nhiều OPTIONS mạnh hơn?
---

- **OpenCV**: Quá phức tạp cho bài này
- **AI APIs** (Stability AI, Replicate): Tốn tiền ($0.01-0.05/ảnh) và chậm
- **ImageMagick**: Phải cài thêm software

→ **Chọn Pillow** vì đơn giản, free, và đủ dùng cho resize cơ bản.

---

## 2. Prompts với Claude (tool mình dùng)

### Prompt 1: Hỏi cách approach
> "Tôi có một bức ảnh 1080x 1920 làm sao tôi resize bức ảnh về 1200x 1920 mà vẫn giữ được high quality cũng như là không làm giãn ảnh."

→ Được 4 cách: crop, stretch, AI inpainting, edge mirroring. Chọn edge mirroring.

### Prompt 2: Implement edge mirroring
> "Làm thế nào để tôi có thể thực hiện cách này" (cách edge mirroring này tôi đã sử dụng trong photoshop trước đó nhiều lần)

→ Học được `transpose(FLIP_LEFT_RIGHT)` và `GaussianBlur`.

### Prompt 3: Batch processing
> "Kết hợp batch processing trong đoạn mã trên, giúp tối ưu quy trình"

→ Có được `sys.argv` và `Path.glob()`.

### Prompt 4-5: Optimize chất lượng
Hỏi về JPEG quality và mirror width → settled on quality=95 và 50px mirror.

**Cái gì work:**
- Hỏi trade-offs trước khi code
- Test nhiều settings khác nhau 

**Cái gì không work:**
- Ban đầu blur=5 quá nhạt, phải tăng lên 15
- Thử content-aware fill nhưng quá phức tạp nên bỏ

---

## 3. Timeline (tổng ~1 giờ)

1. **Research** (10 phút): So sánh các cách resize, chọn edge mirroring
2. **Setup** (5 phút): Cài Pillow, tạo test images
3. **Code core logic** (20 phút): Canvas + mirror + blur
4. **Batch processing** (10 phút): Handle folders với glob
5. **Testing & tuning** (15 phút): Test vài ảnh, điều chỉnh blur từ 5→15, quality 95

---

## 4. Technical Decisions

### Tại sao edge mirroring thay vì AI?
- Đơn giản hơn
- Free (AI tốn $0.01-0.05/ảnh)
- Đủ tốt cho 85% trường hợp

### Settings cuối cùng:
- **Blur radius**: 15px (test 5→10→15, 15 là natural nhất)
- **JPEG quality**: 95% (balance giữa quality và file size)
- **Mirror width**: 50px (đủ chi tiết, không lặp lại rõ)

### Nếu có thêm thời gian sẽ làm:
- Auto detect edges phức tạp → fallback sang crop
- Gradient blend thay vì uniform blur
- Giữ nguyên format gốc (PNG → PNG)

---

## 5. Results

### Work tốt với:
✅ Portraits (background mờ)
✅ Landscapes (trời, biển)
✅ Product photos (nền đơn giản)

### Hạn chế:
❌ Ảnh có chữ ở cạnh → chữ bị mirror ngược
❌ Pattern phức tạp ở cạnh → thấy rõ lặp lại
❌ High contrast edges → nhìn thấy đường nối

### Stats:
- **Tốc độ**: ~0.5-1s/ảnh
- **Success rate**: 85% natural, 15% có artifacts
- **File size**: Tăng 10-15% so với gốc

---

## 6. Cost

**Solution hiện tại:**
- $0/ảnh
- 1000 ảnh = $0, ~10 phút

**Nếu dùng AI:**
- $0.01-0.02/ảnh
- 1000 ảnh = $10-20, ~30-60 phút

→ Pillow rẻ hơn và nhanh hơn nhiều.

---

## 7. Đánh giá thật

**Good:**
- Solution đơn giản, work được
- Không tốn tiền
- Nhanh

**Not so good:**
- Không smart như AI (không hiểu content)
- 15% ảnh có artifacts
- Phải manual check quality

**Production ready?**
- MVP: OK luôn
- Production: Cần thêm AI fallback cho edge cases
- Client work: OK nếu họ biết limitations

---

## Kết
Bài này mình approach practical - chọn tool đủ dùng thay vì over-engineer với AI. 1 giờ chủ yếu code và test nhanh blur settings. Nếu làm production app thật, mình sẽ thêm AI inpainting cho 15% ảnh mà edge mirroring không ổn.