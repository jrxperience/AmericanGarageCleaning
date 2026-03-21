import re

with open('src/index.html', 'r') as f:
    content = f.read()

# Fix unencoded ampersands
content = re.sub(r'(?<!&)&(?!amp;|lt;|gt;|#8209;|&nbsp;)', r'&amp;', content)

# Fix tel non-breaking spaces and hyphens
content = re.sub(r'\(602\)\s*767-3546', r'(602)&nbsp;767&#8209;3546', content)
content = re.sub(r'\(602\) 767-3546', r'(602)&nbsp;767&#8209;3546', content)

# Fix unclosed divs by finding the open ones in index.html, they appear to be in the sticky cta or mobile menu
content = re.sub(r'<div class="bar > span"', r'<div class="bar &gt; span"', content)
content = re.sub(r'</section>\s+<section id="proof">', r'</div>\n      </section>\n      <section id="proof">', content)

# Fix void tags
content = re.sub(r'<img(.*?)\s*/>', r'<img\1>', content)
content = re.sub(r'<input(.*?)\s*/>', r'<input\1>', content)

# Fix missing button types
content = re.sub(r'<button class="burger"', r'<button type="button" class="burger"', content)
content = re.sub(r'<button class="btn primary"', r'<button type="submit" class="btn primary"', content)
content = re.sub(r'<button class="carouselNav', r'<button type="button" class="carouselNav', content)
content = re.sub(r'<button class="scrollTopBtn', r'<button type="button" class="scrollTopBtn', content)

# Fix trailing whitespaces
content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

# Fix aria-label misuse on progress and divs
content = re.sub(r'<div class="progress" aria-label="Form progress">', r'<div class="progress" role="progressbar" aria-label="Form progress">', content)
content = re.sub(r'<div class="mobileMenu" id="mobileMenu" aria-label="Mobile menu">', r'<nav class="mobileMenu" id="mobileMenu" aria-label="Mobile menu">', content)
content = re.sub(r'<div class="scrollTopBtn', r'<button type="button" class="scrollTopBtn', content)

# Fix missing input types
content = re.sub(r'<input id="address" name="address" placeholder="Property Address" required>', r'<input type="text" id="address" name="address" placeholder="Property Address" required>', content)
content = re.sub(r'<input id="email" name="email" placeholder="Email Address" required>', r'<input type="email" id="email" name="email" placeholder="Email Address" required>', content)

# Fix long title
content = re.sub(r'<title>Phoenix Commercial Parking Garage &amp;amp; Lot Cleaning</title>', r'<title>Phoenix Commercial Garage Cleaning</title>', content)


with open('src/index.html', 'w') as f:
    f.write(content)
