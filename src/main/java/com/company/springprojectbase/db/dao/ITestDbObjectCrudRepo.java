package com.company.springprojectbase.db.dao;

import com.company.springprojectbase.db.models.TestDBObject;
import org.springframework.data.repository.CrudRepository;

public interface ITestDbObjectCrudRepo extends CrudRepository<TestDBObject, Integer> {}
