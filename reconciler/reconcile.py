from reconciler.webutils import parse_raw_results, return_reconciled_raw
import pandas as pd


def reconcile(
    column_to_reconcile,
    type_id,
    top_res=1,
    reconciliation_endpoint="https://wikidata.reconci.link/en/api",
):
    """
    Reconcile a DataFrame column

    This is the main function of this package, it takes in a Pandas Series,
    that is, a column of a DataFrame, and sends it for reconciliation. In
    order to return more confident results, the parameter type_id corresponds
    to the type of item you're trying to reconcile against, that is, in case of a Wikidata item,
    it is the item's 'instance of' property. There is also a top_res argument,
    to filter the retrieved matches, this can be either an int, corresponding to the number of
    matches you want to retrieve for each reconciled item, or 'all', to return all matches.
    The reconciliation_endpoint argument corresponds to the reconciliation service you're
    trying to access, if no value is given, it will default to the Wikidata reconciliation
    endpoint. See <https://reconciliation-api.github.io/testbench/> for a list of available
    endpoints.

    The time this function takes to run will depend on the number of unique items
    you have on your column, keep in mind that if you have a very large DataFrame, it
    may be easier to break it up in smaller pieces and reconcile each one individually.

    Args:
        column_to_reconcile (Series): A pandas Series corresponding to
            the column to be reconciled.
        type_id (str): The item type to reconcile against, in case of a
            wikidata item, it corresponds to the item's 'instance of' QID.
        top_res (int or str): The maximum number of matches to return for
            each reconciled item, defaults to one. To retrieve all matches,
            set it to 'all'.
        reconciliation_endpoint (str): The reconciliation endpoint, defaults
            to the Wikidata reconciliation endpoint.

    Returns:
        DataFrame: A Pandas DataFrame with the reconciled results.

    Raises:
        ValueError: top_res argument must be one of either 'all' or an integer.
    """
    input_keys, response = return_reconciled_raw(
        column_to_reconcile, type_id, reconciliation_endpoint
    )

    parsed = parse_raw_results(input_keys, response)

    full_df = parsed.drop(["features"], axis=1)

    if top_res == "all":
        return full_df
    elif isinstance(top_res, int):
        filtered = full_df.groupby("input_value").head(top_res).reset_index(drop=True)
        return filtered
    else:
        raise ValueError("top_res argument must be one of either 'all' or an integer")