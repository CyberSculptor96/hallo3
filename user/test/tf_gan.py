import tensorflow_gan as tfgan

def calculate_fvd(real_activations,
                  generated_activations):
  """Returns a list of ops that compute metrics as funcs of activations.

  Args:
    real_activations: <float32>[num_samples, embedding_size]
    generated_activations: <float32>[num_samples, embedding_size]

  Returns:
    A scalar that contains the requested FVD.
  """
  return tfgan.eval.frechet_classifier_distance_from_activations(
      real_activations, generated_activations)