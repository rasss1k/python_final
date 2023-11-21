const sliders = document.querySelectorAll('.slider__item');
const prevBtn = document.querySelector('.prev__btn');
const nextBtn = document.querySelector('.next__btn');
const dots = document.querySelectorAll('.dot__item');
let index = 0;

const showSliders = (n) => {
    for(slide of sliders) {
        slide.classList.remove('active');
    }
    sliders[n].classList.add('active')
}

const nextSlide = () => {
    if (index == sliders.length - 1){
        index = 0;
        showSliders(index);
        showDots(index);
    } else {
        index++;
        showSliders(index);
        showDots(index);
    }
}

const prevSlide = () => {
    if (index == 0){
        index = sliders.length -1;
        showSliders(index);
        showDots(index);
    } else {
        index--;
        showSliders(index);
        showDots(index);
    }
}

const showDots = (n) => {
    for(dot of dots){
        dot.classList.remove('active');
    }
    dots[n].classList.add('active');
}

dots.forEach((dot, indexDot) => {
    dot.addEventListener('click', () => {
        index = indexDot;
        showSliders(index);
        showDots(index);
    })
})


let tabsHeader = document.querySelectorAll('.tabs__header__item');
tabsHeader.forEach((item) => {
    item.addEventListener('click', function() {
        let tabTitle = this.dataset.tab;
        let tabContent = document.querySelector('.tabs__content__item[data-tab="' + tabTitle + '"]');

        document.querySelectorAll('.tabs__content__item').forEach((item) =>{
            item.classList.remove('active')
        })
        tabsHeader.forEach((item) => {
            item.classList.remove('active')
        })

        tabContent.classList.add('active');
        this.classList.add('active');
    })
})


nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);   