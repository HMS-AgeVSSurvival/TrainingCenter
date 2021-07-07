function onOpen(e) {
    let ui = SpreadsheetApp.getUi();
  
    let subMenuR2 = ui.createMenu("Report r²").addItem("Examination", "reportR2Examination").addItem("Laboratory", "reportR2Laboratory").addItem("Questionnaire", "reportR2Questionnaire");
  
    let subMenuCindexes = ui.createMenu("Report C-indexes").addItem("Examination", "reportCindexesExamination").addItem("Laboratory", "reportCindexesLaboratory").addItem("Questionnaire", "reportCindexesQuestionnaire");
    
    ui.createMenu("Fill Summary").addItem("Report Age range", "reportAgeRange").addItem("Report Shape", "reportShape").addSubMenu(subMenuR2).addSubMenu(subMenuCindexes).addToUi();
}
  