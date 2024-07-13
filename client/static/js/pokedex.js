function navigateTo(url) {
    window.location.href = url;
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    const categoryList = document.querySelector('.category');
    const items = document.querySelectorAll('.card');
    const itemWidth = items[0].clientWidth + 20; // width + margin

    let scrollPos = 0;

    const scrollContainer = (direction) => {
        if (direction === 'right') {
            scrollPos += itemWidth;
            if (scrollPos >= categoryList.scrollWidth) {
                scrollPos = 0;
            }
        } else if (direction === 'left') {
            scrollPos -= itemWidth;
            if (scrollPos < 0) {
                scrollPos = categoryList.scrollWidth - container.clientWidth;
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
