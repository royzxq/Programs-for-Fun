//
//  NeuralNets.h
//  NeuralNets
//
//  Created by XinquanZhou on 6/24/15.
//  Copyright (c) 2015 Xinquan Zhou. All rights reserved.
//

#ifndef __NeuralNets__NeuralNets__
#define __NeuralNets__NeuralNets__

#include <stdio.h>
#include <vector>
#include <Eigen/Core>

//class MatrixXf;

class NeuralNets {
private:
    float _learning_rate;
    size_t _width_in_pixels;
    size_t _num_hidden_nodes;
    size_t _num_input, _num_output;
    size_t _num_sample;
    Eigen::MatrixXf _data_matrix;
    Eigen::MatrixXf _weights1, _weights2;
    Eigen::ArrayXf _bias1, _bias2;
    std::vector<int> _labels;
    bool _use_file;
    
    Eigen::ArrayXf _sigmoid_scalar(Eigen::ArrayXf& z);
    Eigen::ArrayXf _sigmoid_prime_scalar(Eigen::ArrayXf& z);
    Eigen::MatrixXf _rand_initialize_weights(size_t size_in, size_t size_out);
    
    float _validate(int start, int end);

    
public:
    // for data_matrix, a row is a sample, a col is a feature dimension
    NeuralNets(size_t num_hidden_nodes, size_t num_input, size_t num_output, Eigen::MatrixXf &data_matrix, std::vector<int> labels, bool use_file);
    
    void Train();
    int Predict(Eigen::ArrayXf &test_data);
    
    float Validate(int num_job);
    void LoadModel();
    void SaveModel();
    
    void SetFile(char * filename);
    void SetLR(float lr);
    
};


#endif /* defined(__NeuralNets__NeuralNets__) */
