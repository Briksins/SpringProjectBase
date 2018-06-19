package com.company.springprojectbase.db.service;

import com.company.springprojectbase.db.models.TestDBObject;

import java.util.List;

public interface ITestDbObjectService {

    public List<TestDBObject> getAll();
    public void add(TestDBObject newObject);
    public TestDBObject getById(Integer id);
    public void delete(TestDBObject currentObject);
}
