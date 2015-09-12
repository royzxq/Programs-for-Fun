//
//  NeuralNets.cpp
//  NeuralNets
//
//  Created by XinquanZhou on 6/24/15.
//  Copyright (c) 2015 Xinquan Zhou. All rights reserved.
//

#include "NeuralNets.h"
#include <cmath>
#include <vector>
#include <future>

Eigen::ArrayXf NeuralNets::_sigmoid_scalar(Eigen::ArrayXf & z){
    return Eigen::ArrayXf::Ones(1,_num_hidden_nodes) / (Eigen::ArrayXf::Ones(1,_num_hidden_nodes) + exp(-z));
}

Eigen::ArrayXf NeuralNets::_sigmoid_prime_scalar(Eigen::ArrayXf& z){
    return _sigmoid_scalar(z) * (Eigen::ArrayXf::Ones(1,_num_hidden_nodes) - _sigmoid_scalar(z));
}

Eigen::MatrixXf NeuralNets::_rand_initialize_weights(size_t size_in, size_t size_out){
    return  Eigen::MatrixXf::Random(size_in, size_in);
}



NeuralNets::NeuralNets(size_t num_hidden_nodes, size_t num_input, size_t num_output, Eigen::MatrixXf& data_matrix, std::vector<int> labels, bool use_file = false):_num_hidden_nodes(num_hidden_nodes), _num_input(num_input), _num_output(num_output), _data_matrix(data_matrix), _labels(labels), _use_file(use_file){
    _learning_rate = 0.1;
    _width_in_pixels = 20;
    if (!_use_file) {
        _weights1 = _rand_initialize_weights(_num_output, _num_hidden_nodes);
        _weights2 = _rand_initialize_weights(_num_hidden_nodes, _num_output);
        _bias1 = _rand_initialize_weights(1, _num_hidden_nodes).array();
        _bias2 = _rand_initialize_weights(1, _num_output).array();
        _num_sample = labels.size();
    }
}

void NeuralNets::Train(){
    for (int i = 0 ; i < _num_sample; i++) {
        Eigen::ArrayXf y1 = _data_matrix.row(i) * _weights1;
        Eigen::ArrayXf sum1 = y1 + _bias1;
//        for (int j = 0 ; j < _num_hidden_nodes; j++) {
//            sum1(j) = _sigmoid_scalar(sum1(j));
//        }
        y1 = _sigmoid_scalar(sum1);
        
        Eigen::ArrayXf y2 = y1.matrix() * _weights2;
        Eigen::ArrayXf sum2 = y2 + _bias2;
        y2 = _sigmoid_scalar(sum2);
        
        Eigen::ArrayXf actual = Eigen::ArrayXf::Zero(1, _num_output);
        actual(_labels[i]) = 1;
        Eigen::ArrayXf Errors = actual - y2;
        Eigen::ArrayXf HiddenErrors = _weights2 * Errors.matrix();
        HiddenErrors = HiddenErrors * y1;
        
        _weights1 += _learning_rate * (HiddenErrors.matrix() * actual.matrix());
        _weights2 += _learning_rate * (Errors.matrix() * y1.matrix());
        
        _bias1 += _learning_rate * Errors;
        _bias2 += _learning_rate * HiddenErrors;
    }
}

int NeuralNets::Predict(Eigen::ArrayXf &test_data){
    Eigen::ArrayXf y1 = test_data.matrix() * _weights1;
    Eigen::ArrayXf sum1 = y1 + _bias1;
    //        for (int j = 0 ; j < _num_hidden_nodes; j++) {
    //            sum1(j) = _sigmoid_scalar(sum1(j));
    //        }
    y1 = _sigmoid_scalar(sum1);
    
    Eigen::ArrayXf y2 = y1.matrix() * _weights2;
    Eigen::ArrayXf sum2 = y2 + _bias2;
    y2 = _sigmoid_scalar(sum2);
    Eigen::ArrayXf::Index minRow;
    y2.minCoeff(&minRow);
    return static_cast<int>(minRow) ;
}

float NeuralNets::_validate(int start, int end){
    // all shared data is read-only, so there is no need to lock
    float res = 0.0 ;
    for (int i = start; i < end; i++) {
        Eigen::ArrayXf y1 = _data_matrix.row(i).array();
        int predict = Predict(y1);
        if (predict == _labels[i]) {
            res += 1;
        }
    }
    return res / (end-start + 1);
}

float NeuralNets::Validate(int num_job = 3){
    std::vector<std::future<float>> jobs;
    int num_per_job = _num_sample / num_job;
    for (int i = 0 ; i < num_job; i++) {
        jobs.push_back(std::async(&NeuralNets::_validate, this, i * num_per_job, (i+1) * num_per_job));
    }
    float res = 0;
    for (int i = 0 ; i < num_job; i++) {
        res += jobs[i].get();
    }
    return res/num_job;
}

void NeuralNets::SetLR(float lr){
    _learning_rate = lr;
}


