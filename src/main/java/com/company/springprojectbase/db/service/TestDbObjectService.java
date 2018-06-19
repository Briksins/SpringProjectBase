package com.company.springprojectbase.db.service;

import com.company.springprojectbase.db.dao.ITestDbObjectCrudRepo;
import com.company.springprojectbase.db.models.TestDBObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class TestDbObjectService implements ITestDbObjectService {

    @Autowired
    public ITestDbObjectCrudRepo db_repo;

    @Override
    public List<TestDBObject> getAll() {
        return (List<TestDBObject>) db_repo.findAll();
    }

    @Override
    public void add(TestDBObject newObject) {
        db_repo.save(newObject);
    }

    @Override
    public TestDBObject getById(Integer id) {
        Optional<TestDBObject> result =  db_repo.findById(id);
        return result.orElse(null);
    }

    @Override
    public void delete(TestDBObject thisObject) {
        db_repo.delete(thisObject);
    }
}
