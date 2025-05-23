from sqlalchemy import orm
from api import db
from api.db_models import Mutation, MutationType
from .database_helpers import build_general_query, general_core_fields

mutation_related_fields = ["gene", "mutation_type", "sample_mutation_assoc", "samples"]
mutation_core_fields = ["id", "name", "gene_id", "mutation_code", "mutation_type_id"]

mutation_code_related_fields = ["driver_results", "mutations"]
mutation_code_core_fields = ["id", "code"]

mutation_type_related_fields = ["mutations"]
mutation_type_core_fields = general_core_fields + ["display"]


def return_mutation_query(*args):
    return build_general_query(
        Mutation,
        args=args,
        accepted_option_args=mutation_related_fields,
        accepted_query_args=mutation_core_fields,
    )


def return_mutation_type_query(*args):
    return build_general_query(
        MutationType,
        args=args,
        accepted_option_args=mutation_type_related_fields,
        accepted_query_args=mutation_type_core_fields,
    )
