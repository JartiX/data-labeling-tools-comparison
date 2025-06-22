import pandas as pd

def preprocess_time_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Предобработка временных данных в DataFrame:
    - Попытка обнаружить и преобразовать столбец с датой и временем.
    - Удаление строк с любыми значениями NaN.
    - Установка столбца с датой и временем в качестве индекса.

    Параметры:
    df (pd.DataFrame): DataFrame, содержащий временные данные.

    Возвращает:
    pd.DataFrame: Очищенный DataFrame с индексом по времени.
    """
    # Попытка использовать столбец 'time', если он существует
    datetime_col = None
    if 'time' in df.columns:
        datetime_col = 'time'
    else:
        # Попытка обнаружить столбец с датой и временем
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                datetime_col = col
                break
            try:
                parsed = pd.to_datetime(df[col], errors='coerce')
                if parsed.notna().sum() > 0:
                    df[col] = parsed
                    datetime_col = col
                    break
            except Exception:
                continue
    
    if datetime_col is None:
        raise ValueError("Не найден подходящий столбец с датой и временем.")

    # Преобразование столбца с датой и временем в формат datetime
    df[datetime_col] = pd.to_datetime(df[datetime_col], errors='coerce')

    # Удаление строк с недопустимыми значениями времени
    df = df.dropna(subset=[datetime_col])

    # Удаление строк с любыми значениями NaN
    df = df.dropna()

    df.set_index(datetime_col, inplace=True)

    return df

df = pd.read_csv('data/time_row/LSTM-Multivariate_pollution.csv')
preprocessed_df = preprocess_time_data(df)

# Сохранение предобработанного DataFrame
preprocessed_df.to_csv('data/time_row/preprocessed_LSTM-Multivariate_pollution.csv')