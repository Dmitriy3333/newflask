    const geoData = [
        {
            country: "Россия",
            regions: [
                { region: "Краснодарский край", resorts: ["Сочи", "Анапа"] },
                { region: "Ставропольский край", resorts: ["Кисловодск", "Ессентуки"] },
                { region: "Алтайский край", resorts: ["Белокуриха", "Горный Алтай"] },
                { region: "Крым", resorts: ["Ялта", "Евпатория"] },
                { region: "Другой", resorts: ["Другой"] }
            ]
        },
        {
            country: "Казахстан",
            regions: [
                { region: "Алматы", resorts: ["Медео", "Шымбулак"] },
                { region: "Астана", resorts: ["Бурабай", "Щучинск"] },
                { region: "Павлодар", resorts: ["Баянаул", "Аксу"] },
                { region: "Другой", resorts: ["Другой"] }
            ]
        },
        {
            country: "Беларусь",
            regions: [
                { region: "Минская область", resorts: ["Несвиж", "Борисов"] },
                { region: "Гродненская область", resorts: ["Гродно", "Лида"] },
                { region: "Брестская область", resorts: ["Брест", "Кобрин"] },
                { region: "Другой", resorts: ["Другой"] }
            ]
        },
        {
            country: "Узбекистан",
            regions: [
                { region: "Ташкент", resorts: ["Чарвак", "Янгибазар"] },
                { region: "Самарканд", resorts: ["Ургут", "Паянда"] },
                { region: "Другой", resorts: ["Другой"] }
            ]
        },
        {
            country: "Другое",
            regions: [
                { region: "Другой", resorts: ["Другой"] }
            ]
        }
    ];

    const countrySelect = document.getElementById("country");
const regionSelect = document.getElementById("region");
const resortSelect = document.getElementById("resort");

const selectedCountry = countrySelect.dataset.selected;
const selectedRegion = regionSelect.dataset.selected;
const selectedResort = resortSelect.dataset.selected;

// Далее логика инициализации:
populateSelect(countrySelect, geoData.map(c => c.country), selectedCountry);
updateRegions(); // внутри неё уже используется selectedRegion и т.д.


    function populateSelect(select, options, selectedValue) {
        select.innerHTML = "";
        for (var i = 0; i < options.length; i++) {
            var option = document.createElement("option");
            option.value = options[i];
            option.text = options[i];
            if (options[i] === selectedValue) {
                option.selected = true;
            }
            select.appendChild(option);
        }
    }

    function updateRegions() {
        var selectedCountryName = countrySelect.value;
        var regions = [];
        for (var i = 0; i < geoData.length; i++) {
            if (geoData[i].country === selectedCountryName) {
                var regionList = geoData[i].regions;
                for (var j = 0; j < regionList.length; j++) {
                    regions.push(regionList[j].region);
                }
                break;
            }
        }
        populateSelect(regionSelect, regions, selectedRegion);
        updateResorts();
    }

    function updateResorts() {
        var selectedCountryName = countrySelect.value;
        var selectedRegionName = regionSelect.value;
        var resorts = [];
        for (var i = 0; i < geoData.length; i++) {
            if (geoData[i].country === selectedCountryName) {
                var regionList = geoData[i].regions;
                for (var j = 0; j < regionList.length; j++) {
                    if (regionList[j].region === selectedRegionName) {
                        resorts = regionList[j].resorts;
                        break;
                    }
                }
                break;
            }
        }
        populateSelect(resortSelect, resorts, selectedResort);
    }

    window.addEventListener("DOMContentLoaded", function() {
        var countries = [];
        for (var i = 0; i < geoData.length; i++) {
            countries.push(geoData[i].country);
        }
        populateSelect(countrySelect, countries, selectedCountry);
        updateRegions();
    });

    countrySelect.addEventListener("change", updateRegions);
    regionSelect.addEventListener("change", updateResorts);



    document.querySelectorAll('.photo').forEach(carousel => {
        const imgWrap = carousel.querySelector('.img-wrap');
        const imgs = carousel.querySelectorAll('.img-wrap img');
        const prevBtn = carousel.querySelector('.prev');
        const nextBtn = carousel.querySelector('.next');
        let idx = 0;

        function showImg() {
            if (idx >= imgs.length) idx = 0;
            if (idx < 0) idx = imgs.length - 1;
            imgWrap.style.transform = `translateX(-${idx * 100}%)`;
        }

        nextBtn.addEventListener('click', (e) => {
            e.stopPropagation();  // Prevents triggering the sanatorium link
            idx++;
            showImg();
        });

        prevBtn.addEventListener('click', (e) => {
            e.stopPropagation();  // Prevents triggering the sanatorium link
            idx--;
            showImg();
        });

        showImg();
    });