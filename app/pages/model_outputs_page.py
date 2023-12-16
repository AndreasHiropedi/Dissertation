import app.globals
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import html, dcc, callback, Input, Output, MATCH
from models.random_forest.random_forest import RandomForest
from models.ridge_regressor.ridge_regressor import RidgeRegressor
from models.mlp.multilayer_perceptron import MultiLayerPerceptron
from models.svm.support_vector_machine import SupportVectorMachine


def create_layout(model_count):
    """
    This function creates all pages for the model outputs.
    """

    # Check if model has been created successfully
    model_key = f'Model {model_count}'

    if app.globals.MODELS_LIST[model_key] is None:
        return html.Div(
            id='output-page',
            children=[
                html.Div(
                    id='output-page-header',
                    children=[
                        html.H1(
                            children=[f"Model {model_count} output"]
                        )
                    ]
                ),
                html.Div(
                    id='output-page-contents',
                    children=[
                        "No content available since the model hasn't been created or initiated."
                    ]
                )
            ]
        )

    return html.Div(
        id='output-page',
        children=[
            html.Div(
                id='output-page-header',
                children=[
                    html.H1(
                        children=[f"Model {model_count} output"]
                    )
                ]
            ),
            html.Div(
                id='output-page-contents',
                children=[
                    model_summary_card(model_count)
                ]
            )
        ]
    )


def model_summary_card(model_count):
    """
    This function generates the card containing the summary information about the respective model
    """

    # Retrieve the model
    model_key = f'Model {model_count}'
    model = app.globals.MODELS_LIST[model_key]

    # Retrieve all necessary summary information

    # Model type
    model_type = ''
    if isinstance(model, RandomForest):
        model_type = 'Random Forest'
    elif isinstance(model, MultiLayerPerceptron):
        model_type = 'Multi-layer Perceptron'
    elif isinstance(model, SupportVectorMachine):
        model_type = 'Support Vector Machine'
    elif isinstance(model, RidgeRegressor):
        model_type = 'Ridge Regressor'

    # Feature selection
    if model.use_feature_select == 'no':
        feature_selection = 'Not enabled'
    else:
        feature_selection = f'{model.feature_number} features selected using {model.feature_selection_algorithm}'

    # Unsupervised learning
    if model.use_unsupervised == 'no':
        unsupervised_learning = 'Not enabled'
    else:
        unsupervised_learning = f'{model.dimensionality_reduction_algorithm} used'

    # Hyperparameter optimization
    if model.use_hyper_opt == 'no':
        hyper_opt = 'Not enabled'
    else:
        hyper_opt = f'Bayesian Hyperparameter Optimization with {model.hyper_opt_iterations} iterations'

    return dbc.Card(
        id={'type': 'model-summary-card', 'index': model_count},
        children=[
            dbc.CardHeader(
                id='card-header-model',
                children=['Summary information']
            ),
            dbc.CardBody(
                id='card-body-model',
                children=[
                    # Model Input Details
                    html.Div(
                        id='card-body-model-info',
                        children=
                        [
                            html.H4(
                                "Model Input Details",
                                style={
                                    'text-align': 'center',
                                }
                            ),
                            html.P(f"Model Type: {model_type}"),
                            html.P(f"Feature Selection: {feature_selection}"),
                            html.P(f"Unsupervised Learning: {unsupervised_learning}"),
                            html.P(f"Hyperparameter Optimization: {hyper_opt}"),
                        ],
                        style={
                            'flex': 1,
                            'display': 'flex',
                            'flex-direction': 'column',
                            'justify-content': 'space-between',
                            'borderRight': '1px solid black',
                            'paddingRight': '10px',
                        }
                    ),

                    # Training Statistics
                    html.Div(
                        id='card-body-model-training',
                        children=
                        [
                            html.H4(
                                "Training Statistics",
                                style={
                                    'text-align': 'center'
                                }
                            ),
                            html.P(f"RMSE: {round(model.training_RMSE, 2)} ± {round(model.training_RMSE_std, 4)}"),
                            html.P(f"R-squared: {round(model.training_R_squared, 2)} ± "
                                   f"{round(model.training_R_squared_std, 4)}"),
                            html.P(f"MAE: {round(model.training_MAE, 2)} ± {round(model.training_MAE_std, 4)}"),
                            html.P(f"Percentage within 2-fold error: {round(model.training_percentage_2fold_error, 2)} "
                                   f"± {round(model.training_percentage_2fold_error_std, 4)}"),
                        ],
                        style={
                            'flex': 1,
                            'display': 'flex',
                            'flex-direction': 'column',
                            'justify-content': 'space-between',
                            'borderRight': '1px solid black',
                            'paddingRight': '10px',
                            'paddingLeft': '10px',
                        }
                    ),

                    # Testing Statistics
                    html.Div(
                        id='card-body-model-testing',
                        children=[
                            html.H4(
                                "Testing Statistics",
                                style={
                                    'text-align': 'center'
                                }
                            ),
                            html.P(f"RMSE: {round(model.testing_RMSE, 2)}"),
                            html.P(f"R-squared: {round(model.testing_R_squared, 2)}"),
                            html.P(f"MAE: {round(model.testing_MAE, 2)}"),
                            html.P(f"Percentage within 2-fold error: {round(model.testing_percentage_2fold_error, 2)}%")
                        ],
                        style={
                            'flex': 1,
                            'display': 'flex',
                            'flex-direction': 'column',
                            'justify-content': 'space-between',
                            'paddingLeft': '10px',
                        }
                    )
                ],
                style={
                    'display': 'flex'
                }
            )
        ],
        style={
            'width': '75%',
            'margin-left': '200px',
            'border': '2px solid black',
            'margin-top': '50px'
        }
    )
