function navigateTo(url) {
    window.location.href = url;
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    const categoryList = document.querySelector('.category');
    const items = document.querySelectorAll('.card');
    const itemWidth = items[0].offsetWidth + 20; // width + margin (includes padding and border if any)

    let scrollPos = 0;
    const maxScroll = categoryList.scrollWidth - container.offsetWidth;

    const scrollContainer = (direction) => {
        if (direction === 'right') {
            scrollPos += itemWidth;
            if (scrollPos > maxScroll) {
                scrollPos = maxScroll; // Prevents scrolling beyond the content
            }
        } else if (direction === 'left') {
            scrollPos -= itemWidth;
            if (scrollPos < 0) {
                scrollPos = 0; // Prevents scrolling before the content
            }
        }
        categoryList.style.transform = `translateX(-${scrollPos}px)`;
    };

    document.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowRight') {
            scrollContainer('right');
        } else if (event.key === 'ArrowLeft') {
            scrollContainer('left');
        }
    });

    window.scrollContainer = scrollContainer; // Expose function to global scope for button clicks
});
