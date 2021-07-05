function onOpen() {
    let ui = SpreadsheetApp.getUi();
    ui.createMenu("Custom actions").addItem("Report Age range", "reportAgeRange").addItem("Report C-indexes", "reportCindexes").addToUi();
}
