#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tensorflow as tf


def data_generator():
    x = "foo"
    y = 0
    yield x, y


def get_dataset():
    return tf.data.Dataset.from_generator(
           data_generator,
           output_types=(tf.uint8, tf.uint32),
           output_shapes=(tf.TensorShape([1654, 2340, 4]), tf.TensorShape([])))
