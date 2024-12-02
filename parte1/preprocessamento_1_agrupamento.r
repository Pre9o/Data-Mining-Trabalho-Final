if (!requireNamespace("readxl", quietly = TRUE)) install.packages("readxl")
library(readxl)

parent_dir <- dirname(current_dir)  # Sobe um nível no diretório
datasets_dir <- file.path(parent_dir, "2025 UFSM datasets")

load_dataset <- function(dataset_name) {
  dataset_path <- file.path(datasets_dir, dataset_name)
  dataset <- readRDS(dataset_path)
  return(dataset)
}

datasets_names <- list.files(datasets_dir)

unique_situacao_values <- c()

for (dataset_name in datasets_names) {
  if (!grepl(".xlsx", dataset_name)) {
    next
  }
  print(dataset_name)
  dataset <- read_excel(file.path(datasets_dir, dataset_name))
  for (i in 1:nrow(dataset)) {
    situacao <- dataset$Situação[i]
    if (situacao %in% unique_situacao_values) {
      next
    }
    unique_situacao_values <- c(unique_situacao_values, situacao)
  }
}

colunas_iniciais <- setdiff(names(dataset), c("Situação", "%", "Alunos"))
colunas_situacao <- paste("Porcentagem de", unique_situacao_values)
dataset_new <- data.frame(matrix(ncol = length(colunas_iniciais) + length(colunas_situacao) + 1, nrow = 0))
colnames(dataset_new) <- c(colunas_iniciais, colunas_situacao, "Alunos")

cod_disciplina <- NULL
cod_turma <- NULL
professor <- NULL
cod_curso <- NULL

for (dataset_name in datasets_names) {
  if (!grepl(".xlsx", dataset_name)) {
    next
  }
  print(dataset_name)
  dataset <- read_excel(file.path(datasets_dir, dataset_name))
  
  for (i in 1:nrow(dataset)) {
    situacao <- dataset$Situação[i]
    if (is.null(cod_disciplina) || cod_disciplina != dataset$`Cód. Disciplina`[i] || cod_turma != dataset$`Cód. Turma`[i] || professor != dataset$Professor[i] || cod_curso != dataset$`Cód. Curso`[i]) {
      new_row <- dataset[i, -which(names(dataset) %in% c("Situação", "%", "Alunos"))]
      for (situacao_value in unique_situacao_values) {
        new_row[paste("Porcentagem de", situacao_value)] <- 0
      }
      new_row["Alunos"] <- 0
      dataset_new <- rbind(dataset_new, new_row)
      cod_disciplina <- dataset$`Cód. Disciplina`[i]
      cod_turma <- dataset$`Cód. Turma`[i]
      professor <- dataset$Professor[i]
      cod_curso <- dataset$`Cód. Curso`[i]
    }
    dataset_new[nrow(dataset_new), paste("Porcentagem de", situacao)] <- as.numeric(dataset$`%`[i])
    dataset_new[nrow(dataset_new), "Alunos"] <- dataset_new[nrow(dataset_new), "Alunos"] + dataset$Alunos[i]
  }
}
print(dataset_new)

write.csv(dataset_new, file = "dataset_unified.csv", row.names = FALSE)