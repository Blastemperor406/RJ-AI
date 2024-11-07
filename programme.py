from hmmlearn.hmm import MultinomialHMM
import numpy as np
def programme():
    # Define the HMM model
    # Initial state probabilities
    initial_probs= np.array([0,0,1]) #(State1=News, State2=Music, State3=Idle Chat)

    # Transition probabilities matrix
    # Each row corresponds to a state and each column corresponds to the probability of transitioning to another state
    # For example, [0.3, 0.3, 0.4] means if currently in "idle chat", there's a 50% chance to stay in "idle chat", 
    # 40% chance to switch to "music", and 20% chance to switch to "news"

    transition_probs= np.array([ [0.1, 0.6, 0.3],  
        [0.4, 0.35, 0.25],  
        [0.35, 0.55, 0.1]]) 

    # Emission probabilities matrix
    # For simplicity, let's assume 3 possible observations: "greeting", "song", "content"
    emission_probs = np.array([
        [0.2, 0.2, 0.6],  # State 1: News
        [0.1, 0.8, 0.1],  # State 2: Music
        [0.7, 0.2, 0.1]   # State 3: Idle Chat

    ])
    states = ["Talk", "song", "News"]

    # Define the model
    model = MultinomialHMM(n_components=len(states),n_trials=10)


    # Set model parameters
    model.startprob_ = initial_probs
    model.transmat_ = transition_probs
    model.emissionprob_ = emission_probs

    # Simulating a radio show sequence
    # Number of steps in the sequence
    n_steps = 10

    # Generate a sequence
    logprob, sequence = model.sample(n_samples=n_steps)


    # Decode the sequence of states
    states_sequence = model.predict(logprob)

    # Print results
    #print("Generated State Sequence:")
    #for i in range(n_steps):
        #print(f"Step {i + 1}: State = {states[states_sequence[i]]}, Observation = {sequence[i]}")

    # Map observation indices to observation names for clarity
    observations = ["News", "song", "Talk"]
    return [observations[int(obs)] for obs in sequence.flatten()]

