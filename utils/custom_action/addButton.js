function onOpen(e) {
    let ui = SpreadsheetApp.getUi();

    let subMenuShapeLaboratory = ui.createMenu("Laboratory").addItem("All", "reportShapeLaboratoryAll").addItem("CVD", "reportShapeLaboratoryCVD").addItem("Cancer", "reportShapeLaboratoryCancer");
    let subMenuShape = ui.createMenu("Report shape").addItem("Examination", "reportShapeExamination").addSubMenu(subMenuShapeLaboratory).addItem("Questionnaire", "reportShapeQuestionnaire");

    let subMenuAgeRangeLaboratory = ui.createMenu("Laboratory").addItem("All", "reportAgeRangeLaboratoryAll").addItem("CVD", "reportAgeRangeLaboratoryCVD").addItem("Cancer", "reportAgeRangeLaboratoryCancer");
    let subMenuAgeRange = ui.createMenu("Report age range").addItem("Examination", "reportAgeRangeExamination").addSubMenu(subMenuAgeRangeLaboratory).addItem("Questionnaire", "reportAgeRangeQuestionnaire");

    let subMenuR2 = ui.createMenu("Report r²").addItem("Examination", "reportR2Examination").addItem("Laboratory", "reportR2Laboratory").addItem("Questionnaire", "reportR2Questionnaire");

    let subSubMenuCindexesLaboratory = ui.createMenu("Laboratory").addItem("All", "reportCindexesLaboratoryAll").addItem("CVD", "reportCindexesLaboratoryCVD").addItem("Cancer", "reportCindexesLaboratoryCancer");
    let subMenuCindexes = ui.createMenu("Report C-indexes").addItem("Examination", "reportCindexesExamination").addSubMenu(subSubMenuCindexesLaboratory).addItem("Questionnaire", "reportCindexesQuestionnaire");

    let subMenuLogHazardRatio = ui.createMenu("Report log Hazard Ratio").addItem("Examination", "reportLogHazardRatioExamination").addItem("Laboratory", "reportLogHazardRatioLaboratory").addItem("Questionnaire", "reportLogHazardRatioQuestionnaire");

    ui.createMenu("Fill Summary").addSubMenu(subMenuShape).addSubMenu(subMenuAgeRange).addSubMenu(subMenuR2).addSubMenu(subMenuCindexes).addSubMenu(subMenuLogHazardRatio).addToUi();
}