package io.werender.examples;

public interface Command<T> {

    public T execute(CommandContext context) throws Exception;

}
