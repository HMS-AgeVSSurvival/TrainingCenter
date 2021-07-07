const mainCategories = ["examination", "laboratory", "questionnaire"];
const targets = ["all", "cvd", "cancer"];


function getSpreadSheet() {
    return SpreadsheetApp.openById("1IZDQmitlE5fU_5wbu2T8jF2_4i7I7Q_VTTjv6buVFwc");
}


function findCell(sheet, name) {
    return sheet.createTextFinder(name).matchEntireCell(true).findNext();
}


function findSpecificCell(sheet, name, number) {
    return sheet.createTextFinder(name).matchEntireCell(true).findAll()[number];
}


function toAlphabet(number) {
    return (number + 9).toString(36).toUpperCase();
}
