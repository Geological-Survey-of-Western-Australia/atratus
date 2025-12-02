from pathlib import Path
import gswa_atratus as gdt

if __name__ == "__main__":
    # setting up loggers
    _ = gdt.setup_logger("known_exceptions", Path(r"logs\TEST - Known Issues.log"))
    _ = gdt.setup_logger("code_issues", Path(r"logs\TEST - Decorator Exceptions.log"))

    # ask us for a select of standard gdt_config files
    config_path = ""

    # connect to the database
    my_db_engine, meta_data = gdt.connect(config_path)

    # load the statmeent from config and convert it to sqla
    columns_dict, joins, aliases = gdt.load_statement_config(config_path)
    my_db_select_metadata = gdt.statement_builder(
        metadata=meta_data,
        engine=my_db_engine,
        columns_dict=columns_dict,
        join_list=joins,
        alias=aliases,
    )

    # query the engine and get a pandas dataframe
    meta_data_df = gdt.select(engine=my_db_engine, statement=my_db_select_metadata)
