if (!requireNamespace("readxl", quietly = TRUE)) install.packages("readxl")
library(readxl)

current_dir <- getwd()
datasets_dir <- file.path(current_dir, "2024 UFSM datasets")

# Rafael Pregardier: Using a function to load the dataset
load_dataset <- function(dataset_name) {
  dataset_path <- file.path(datasets_dir, dataset_name)
  dataset <- readRDS(dataset_path)
  return(dataset)
}

# Rafael Pregardier: Saving all datasets names in a list.
datasets_names <- list.files(datasets_dir)

# Rafael Pregardier: Loading one dataset to modify it.
unique_situacao_values <- c()

for (dataset_name in datasets_names) {
  if (!grepl(".xlsx", dataset_name)) {
    next
  }
  print(dataset_name)
  dataset <- read_excel(file.path(datasets_dir, dataset_name))
  # Rafael Pregardier: For each dataset, it will be checked if the value of "Situação" is already in the list of unique values, if not, it will be added.
  for (i in 1:nrow(dataset)) {
    situacao <- dataset$Situação[i]
    if (situacao %in% unique_situacao_values) {
      next
    }
    unique_situacao_values <- c(unique_situacao_values, situacao)
  }
}

# Rafael Pregardier: Initialize dataset_new with the appropriate columns.
colunas_iniciais <- setdiff(names(dataset), c("Situação", "%", "Alunos"))
colunas_situacao <- paste("Porcentagem de", unique_situacao_values)
dataset_new <- data.frame(matrix(ncol = length(colunas_iniciais) + length(colunas_situacao) + 1, nrow = 0))
colnames(dataset_new) <- c(colunas_iniciais, colunas_situacao, "Alunos")

# Rafael Pregardier: Initialize variables to store the values of "Cód. Disciplina" , Cód. Turma", "Professor" and "Cód. Curso".
cod_disciplina <- NULL
cod_turma <- NULL
professor <- NULL
cod_curso <- NULL

# Rafael Pregardier: A new variable dataset will be created where the "Situação" column will not exist, but instead a column for each unique value of "Situação" with the name "% de" + unique value of "Situação".
# In the first row of each dataset, the values of "Cód. Disciplina", "Cód. Turma", "Professor" and "Cód. Curso" will be taken and saved in variables. For each row of the original dataset, the value of "Situação" will be checked and the value of the "%" column will be saved in a variable with the name "% de" + value of "Situação".
# For each row, the value of "Cód. Disciplina", "Cód. Turma", "Professor" and "Cód. Curso" will be compared with the values saved in the first row. If they are the same, the value of "%" will be saved in the variable with the name "% de" + value of "Situação".
# If the saved variables for comparison are different, a new row will be created in the new dataset with the values of the row in the original dataset, except for the "Situação" column, and with the value of "%" saved in the variable with the name "% de" + value of "Situação".
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