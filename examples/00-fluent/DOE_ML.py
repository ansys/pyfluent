# /// script
# dependencies = [
#   "ansys-fluent-core",
#   "matplotlib",
#   "numpy",
#   "pandas",
#   "plotly",
#   "scikit-learn",
#   "seaborn",
#   "tensorflow",
# ]
# ///

# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""".. _doe_ml:

Design of Experiments and Machine Learning model building
---------------------------------------------------------
"""

#######################################################################################
# Objective
# =====================================================================================
#
# Water enters a Mixing Elbow from two Inlets; Hot (313 K) and Cold (293 K) and exits
# from Outlet. Using PyFluent in the background, this example runs Design of Experiments
# (DOE) with Cold Inlet Velocity and Hot Inlet Velocity as Input Parameters and Outlet
# Temperature as an Output Parameter.
#
# Results can be visualized using a Response Surface. Finally, Supervised Machine
# Learning Regression Task is performed to build the ML Model.
#
# This example demonstrates:
#
# * Design of Experiment, Fluent setup and simulation using PyFluent.
# * Building of Supervised Machine Learning Model.

###################################
# Import required libraries/modules
# =================================

# flake8: noqa: E402

import itertools
import json
from pathlib import Path
from typing import TYPE_CHECKING, cast

from ansys.units import Quantity
from ansys.units.quantity import ArrayLike
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import seaborn as sns
# import tensorflow as tf
# from tensorflow import keras

import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.core.generated.solver.settings_builtin import SurfaceIntegrals
from ansys.fluent.core.generated.solver.settings_builtin_261 import iterate, read_case
from ansys.fluent.core.solver import Initialization, VelocityInlet, RunCalculation
from ansys.units.common import m, s

###########################################################################
# Specifying save path
# ====================

import_filename = examples.download_file(
    "elbow.cas.h5",
    "pyfluent/examples/DOE-ML-Mixing-Elbow",
    save_path=Path.cwd(),
)

#######################
# Fluent Solution Setup
# =====================

#################################################################
# Launch Fluent session with solver mode and print Fluent version
# ===============================================================

solver = pyfluent.Solver.from_install(
    precision=pyfluent.Precision.SINGLE,
    processor_count=4,
)
print(solver.get_fluent_version())


#############################################################################
# Read case
# =========

solver.upload(import_filename)
read_case(solver, file_name=import_filename)

##############################################################################################
# Design of Experiments
# =====================

# Specify inlet velocities for the cold and hot streams.
# Each pair of (cold_value, hot_value) will be used to run one Fluent case.
cold_velocities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7] * m / s

hot_velocities = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0] * m / s


# Allocate a results array. Entry (i, j) will hold the Mass‑Weighted
# Average Temperature at the outlet for cold_velocities[i] and hot_velocities[j].
results = np.zeros((len(cold_velocities), len(hot_velocities)))

for (idx1, cold_value), (idx2, hot_value) in itertools.product(
    enumerate(cold_velocities), enumerate(hot_velocities)
):
    cold_inlet = VelocityInlet.get(solver, name="cold-inlet")
    cold_inlet.momentum.velocity = cold_value

    hot_inlet = VelocityInlet.get(solver, name="hot-inlet")
    hot_inlet.momentum.velocity = hot_value

    initialize = Initialization(solver)
    initialize.initialization_type = "standard"
    initialize.standard_initialize()

    iterate(solver,iter_count=200)

    temperatures = SurfaceIntegrals(solver).get_mass_weighted_avg(
        surface_names=["outlet"], report_of="temperature"
    )

    results[idx1][idx2] = temperatures["outlet"]

##############################################################################################
# Close the session
# =================

solver.exit()

####################################
# Plot Response Surface using Plotly
# ==================================

fig = go.Figure(data=[go.Surface(z=results.T, x=cold_velocities, y=hot_velocities)])

fig.update_layout(
    title={
        "text": "Mixing Elbow Response Surface",
        "y": 0.9,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
    }
)

fig.update_layout(
    scene={
        "xaxis_title": "Cold Inlet Vel (m/s)",
        "yaxis_title": "Hot Inlet Vel (m/s)",
        "zaxis_title": "Outlet Temperature (K)",
    },
    width=600,
    height=600,
    margin={"l": 80, "r": 80, "b": 80, "t": 80},
)
fig.show()


#####################################
# Supervised ML for a Regression Task
# ===================================

############################################
# Create Pandas Dataframe for ML Model Input
# ==========================================
df = pd.DataFrame({"cold_velocities": [], "hot_velocities": [], "result": []})


for (idx1, cold_vel_val), (idx2, hot_vel_val) in itertools.product(
    enumerate(cold_velocities), enumerate(hot_velocities)
):
    df["cold_velocities"].append(cold_vel_val)
    df["hot_velocities"].append(hot_vel_val)
    df["result"].append(results[idx1][idx2])


from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

####################################################################
# Using scikit-learn
# ==================
# * Prepare Features (X) and Label (y) using a Pre-Processing Pipeline
# * Train-Test (80-20) Split
# * Add Polynomial Features to improve ML Model

poly_features = PolynomialFeatures(degree=2, include_bias=False)

transformer1 = Pipeline(
    [
        ("poly_features", poly_features),
        ("std_scaler", StandardScaler()),
    ]
)


x_ct = ColumnTransformer(
    [
        ("transformer1", transformer1, ["cold_velocities", "hot_velocities"]),
    ],
    remainder="drop",
)

train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

X_train = x_ct.fit_transform(train_set)
X_test = x_ct.fit_transform(test_set)

y_train = train_set["result"]
y_test = test_set["result"]
y_train = np.ravel(y_train.T)
y_test = np.ravel(y_test.T)


####################################################
# * Define functions for:
# * Cross-Validation and Display Scores (scikit-learn)
# * Training the Model (scikit-learn)
# * Prediction on Unseen/Test Data (scikit-learn)
# * Parity Plot (Matplotlib and Seaborn)

from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold, cross_val_score

# optionally chose which model to use
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor

if TYPE_CHECKING:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from xgboost import XGBRegressor

np.set_printoptions(precision=2)
out_file = Path.cwd() / "PyFluent_Output.csv"


def display_scores(scores: np.ndarray):
    """Display scores."""
    print("\nCross-Validation Scores:", scores)
    print(f"Mean:{scores.mean():0.2f}")
    print(f"Std. Dev.:{scores.std():0.2f}")


def fit_and_predict(model: LinearRegression | XGBRegressor | RandomForestRegressor):
    """Fit and predict."""
    cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=42)
    cv_scores = cross_val_score(
        model, X_train, y_train, scoring="neg_mean_squared_error", cv=cv
    )
    rmse_scores = np.sqrt(-cv_scores)
    display_scores(rmse_scores)

    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    print(train_predictions.shape[0])
    print("\n\nCoefficient Of Determination")
    print(f"Train Data R2 Score: {r2_score(train_predictions, y_train):0.3f}")
    print(f"Test Data R2 Score: {r2_score(test_predictions, y_test):0.3f}")
    print(
        "\n\nPredictions - Ground Truth (Kelvin): ", (test_predictions - y_test), "\n"
    )

    com_train_set = train_set
    com_test_set = test_set

    train_list = ["train"] * cast(int, train_predictions.shape[0])
    test_list = ["test"] * cast(int, test_predictions.shape[0])

    com_train_set["result"] = train_predictions.tolist()
    com_train_set["set"] = train_list
    com_test_set["result"] = test_predictions.tolist()
    com_test_set["set"] = test_list

    df_combined = pd.concat([com_train_set, com_test_set])

    df_combined.to_csv(out_file, header=True, index=False)

    fig = plt.figure(figsize=(12, 5))

    fig.add_subplot(121)
    sns.regplot(x=y_train, y=train_predictions, color="g")
    plt.title("Train Data", fontsize=16)
    plt.xlabel("Ground Truth", fontsize=12)
    plt.ylabel("Predictions", fontsize=12)

    fig.add_subplot(122)
    sns.regplot(x=y_test, y=test_predictions, color="g")
    plt.title("Unseen Data", fontsize=16)
    plt.xlabel("Ground Truth", fontsize=12)
    plt.ylabel("Predictions", fontsize=12)

    plt.tight_layout()
    plt.show()


#############################################################################
# Select the Model from Linear, Random Forest or XGBoost
# ======================================================
# * Call fit_and_predict

# model = LinearRegression()
# model = RandomForestRegressor(random_state=42)
model = XGBRegressor(
    n_estimators=100, max_depth=10, eta=0.3, subsample=0.8, random_state=42
)

fit_and_predict(model)

#############################################################################
# Show graph
# ==========

plt.show()

# %%
# .. image:: ../../_static/doe_ml_predictions_regression.png
#    :align: center
#    :alt: Regression Model Predictions

# %%
#    Regression Model Predictions

###########################################################
# 3D Visualization of Model Predictions on Train & Test Set
# =========================================================

df = pd.read_csv(out_file)

fig = px.scatter_3d(
    df, x="cold_velocities", y="hot_velocities", z="result", color="set"
)
fig.update_traces(marker={"size": 4})
fig.update_layout(legend={"yanchor": "top", "y": 1, "xanchor": "left", "x": 0.0})

fig.add_traces(go.Surface(z=results.T, x=cold_velocities, y=hot_velocities))

fig.update_layout(
    title={
        "text": "Mixing Elbow Response Surface",
        "y": 0.9,
        "x": 0.5,
        "xanchor": "center",
        "yanchor": "top",
    }
)

fig.update_layout(
    scene={
        "xaxis_title": "Cold Inlet Vel (m/s)",
        "yaxis_title": "Hot Inlet Vel (m/s)",
        "zaxis_title": "Outlet Temperature (K)",
    },
    width=500,
    height=500,
    margin={"l": 80, "r": 80, "b": 80, "t": 80},
)

fig.show()

################################################
# TensorFlow and Keras Neural Network Regression
# ==============================================

print("TensorFlow version is:", tf.__version__)
keras.backend.clear_session()
np.random.seed(42)
tf.random.set_seed(42)

model = keras.models.Sequential(
    [
        keras.layers.Dense(
            20,
            activation="relu",
            input_shape=X_train.shape[1:],
            kernel_initializer="lecun_normal",
        ),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(20, activation="relu", kernel_initializer="lecun_normal"),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(20, activation="relu", kernel_initializer="lecun_normal"),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(1),
    ]
)

optimizer = tf.keras.optimizers.Adam(learning_rate=0.1, beta_1=0.9, beta_2=0.999)

model.compile(loss="mean_squared_error", optimizer=optimizer)
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    "my_keras_model.h5", save_best_only=True
)
early_stopping_cb = keras.callbacks.EarlyStopping(
    patience=30, restore_best_weights=True
)

model.summary()

# keras.utils.plot_model(model, show_shapes=True,) # to_file='dot_img.png', )

history = model.fit(
    X_train,
    y_train,
    epochs=250,
    validation_split=0.2,
    callbacks=[checkpoint_cb, early_stopping_cb],
)
model = keras.models.load_model("my_keras_model.h5")

print(history.params)

pd.DataFrame(history.history).plot(figsize=(8, 5))
plt.grid(True)
plt.show()

train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)
train_predictions = np.ravel(train_predictions.T)
test_predictions = np.ravel(test_predictions.T)
print(test_predictions.shape)

print(f"\n\nTrain R2: {r2_score(train_predictions, y_train):0.3f}")
print(f"Test R2: {r2_score(test_predictions, y_test):0.3f}")
print("Predictions - Ground Truth (Kelvin): ", (test_predictions - y_test))

fig = plt.figure(figsize=(12, 5))

fig.add_subplot(121)
sns.regplot(x=y_train, y=train_predictions, color="g")
plt.title("Train Data", fontsize=16)
plt.xlabel("Ground Truth", fontsize=12)
plt.ylabel("Predictions", fontsize=12)

fig.add_subplot(122)
sns.regplot(x=y_test, y=test_predictions, color="g")
plt.title("Test/Unseen Data", fontsize=16)
plt.xlabel("Ground Truth", fontsize=12)
plt.ylabel("Predictions", fontsize=12)

plt.tight_layout()


#############################################################################
# Show graph
# ==========

plt.show()

# %%
# .. image:: ../../_static/doe_ml_validation_loss.png
#    :align: center
#    :alt: Neural Network Validation Loss

# %%
#    Neural Network Validation Loss

# %%
# .. image:: ../../_static/doe_ml_predictions_neural_network.png
#    :align: center
#    :alt: Neural Network Predictions

# %%
#    Neural Network Predictions
